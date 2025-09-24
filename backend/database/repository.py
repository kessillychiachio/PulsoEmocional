from typing import List, Optional
from sqlalchemy.orm import Session
from models import Analise

def salvar_analise(db: Session, texto: str, polaridade: str, origem: str, confianca: Optional[float]) -> Analise:
    a = Analise(texto=texto, polaridade=polaridade, origem=origem, confianca=confianca)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def listar_analises(db: Session, limit: int, offset: int) -> List[Analise]:
    return db.query(Analise).order_by(Analise.id.desc()).offset(offset).limit(limit).all()