from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal
from classificador_youtube import construir_url_comentarios, buscar_comentarios, classificar_comentarios
from inicializacao_IA import iniciar_IA
from classificador import classificar
from db import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from repository import salvar_analise, listar_analises

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YoutubeReq(BaseModel):
    video_id: str = Field(min_length=5)
    n: int = Field(ge=1, le=60, default=60)

class Comentario(BaseModel):
    Texto: str

class Classificado(BaseModel):
    Texto: str
    Polaridade: Literal["POSITIVO","NEGATIVO","NEUTRO","OUTRO","DESCONHECIDO","erro"] = "OUTRO"

class YoutubeResp(BaseModel):
    comentarios: List[Comentario]
    classificados: List[Classificado]

class ClassificarReq(BaseModel):
    texto: str = Field(min_length=1)
    exemplos_positivos: List[str] | None = None
    exemplos_negativos: List[str] | None = None
    exemplos_neutros: List[str] | None = None

class ClassificarResp(BaseModel):
    Texto: str
    Polaridade: Literal["POSITIVO","NEGATIVO","NEUTRO","OUTRO","erro"]

class AnaliseItem(BaseModel):
    id: int
    Texto: str
    Polaridade: Literal["POSITIVO","NEGATIVO","NEUTRO","OUTRO","DESCONHECIDO","erro"]
    Origem: Literal["manual","youtube"]
    Confianca: float | None
    CriadoEm: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)
    ok, ia = iniciar_IA()
    if not ok:
        raise RuntimeError("Falha ao iniciar IA")
    app.state.ia_modelo = ia

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/youtube/processar", response_model=YoutubeResp)
def processar(req: YoutubeReq, db: Session = Depends(get_db)):
    ok_url, url = construir_url_comentarios(req.video_id, req.n)
    if not ok_url or not url:
        raise HTTPException(status_code=400, detail="Falha ao montar URL do YouTube")
    ok_com, comentarios = buscar_comentarios(url)
    if not ok_com or not comentarios:
        raise HTTPException(status_code=502, detail="Falha ao obter comentários do YouTube")
    ia = getattr(app.state, "ia_modelo", None)
    if ia is None:
        raise HTTPException(status_code=500, detail="IA não inicializada")
    classificados = classificar_comentarios(comentarios, ia)
    for c in classificados:
        texto = c.get("Texto") or ""
        pol = c.get("Polaridade") or "OUTRO"
        salvar_analise(db, texto=texto, polaridade=pol, origem="youtube", confianca=None)
    return {"comentarios": comentarios, "classificados": classificados}

@app.post("/api/classificar/texto", response_model=ClassificarResp)
def api_classificar_texto(req: ClassificarReq, db: Session = Depends(get_db)):
    texto = req.texto.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Texto vazio")
    ia = getattr(app.state, "ia_modelo", None)
    if ia is None:
        raise HTTPException(status_code=500, detail="IA não inicializada")
    ok, rotulo = classificar(
        ia,
        texto,
        exemplos_positivos=req.exemplos_positivos or [],
        exemplos_negativos=req.exemplos_negativos or [],
        exemplos_neutros=req.exemplos_neutros or [],
    )
    if not ok or not isinstance(rotulo, dict):
        salvar_analise(db, texto=texto, polaridade="erro", origem="manual", confianca=None)
        return {"Texto": texto, "Polaridade": "erro"}
    pol = str(rotulo.get("polaridade") or "").strip().upper() or "OUTRO"
    if pol not in {"POSITIVO","NEGATIVO","NEUTRO"}:
        pol = "OUTRO"
    salvar_analise(db, texto=texto, polaridade=pol, origem="manual", confianca=None)
    return {"Texto": texto, "Polaridade": pol}

@app.get("/api/analises", response_model=List[AnaliseItem])
def api_listar_analises(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    rows = listar_analises(db, limit=limit, offset=offset)
    out = []
    for r in rows:
        out.append({
            "id": r.id,
            "Texto": r.texto,
            "Polaridade": r.polaridade,
            "Origem": r.origem,
            "Confianca": r.confianca,
            "CriadoEm": r.criado_em.isoformat()
        })
    return out