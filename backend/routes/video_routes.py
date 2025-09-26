from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.services.video_service import (
    analisar_video_sincrono,
    obter_video_analisado,
    deletar_video_por_id
)
from backend.services import crud
router = APIRouter(prefix="/videos", tags=["Vídeos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analisar")
def iniciar_analise_video(
    video_id: str,
    n_comentarios: int = 60,
    db: Session = Depends(get_db)
):
    return analisar_video_sincrono(db, video_id, n_comentarios)

@router.get("/{video_id_youtube}")
def obter_analise_video(
    video_id_youtube: str,
    db: Session = Depends(get_db)
):
    return obter_video_analisado(db, video_id_youtube)

@router.delete("/{video_id_youtube}")
def deletar_analise_video(
    video_id_youtube: str,
    db: Session = Depends(get_db)
):
    sucesso = deletar_video_por_id(db, video_id_youtube)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado.")
    
    return {"message": f"Vídeo '{video_id_youtube}' e seus comentários foram deletados com sucesso."}

