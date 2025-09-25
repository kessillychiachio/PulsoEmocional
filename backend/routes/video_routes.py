from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.services.video_service import (
    iniciar_analise_completa,
    obter_video_analisado
)

router = APIRouter(prefix="/videos", tags=["Vídeos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analisar")
async def iniciar_analise_video(
    video_id: str,
    background_tasks: BackgroundTasks,
    n_comentarios: int = 60,
    db: Session = Depends(get_db)
):
    return iniciar_analise_completa(db, video_id, n_comentarios, background_tasks)

@router.get("/{video_id_youtube}")
async def obter_analise_video(
    video_id_youtube: str,
    db: Session = Depends(get_db)
):
    return obter_video_analisado(db, video_id_youtube)