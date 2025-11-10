from typing import List
from sqlalchemy.orm import Session
from backend.models.video_models import Video, Comentario

def criar_video(db: Session, video_id_youtube: str) -> Video:
    video = Video(video_id_youtube=video_id_youtube)
    db.add(video)
    db.flush()
    return video

def salvar_comentario(db: Session, video_id: int, texto: str, polaridade: str, emocao: str) -> Comentario:
    comentario = Comentario(
        texto=texto,
        polaridade=polaridade,
        emocao=emocao,
        video_id=video_id
    )
    db.add(comentario)
    return comentario

def salvar_resumo(db: Session, video_id: int, resumo: str) -> Video:
    video = db.query(Video).filter(Video.id == video_id).first()
    if video:
        video.resumo = resumo
    return video

def listar_comentarios(db: Session, video_id: int) -> List[Comentario]:
    return db.query(Comentario).filter(Comentario.video_id == video_id).all()

def listar_videos(db: Session, limit: int = 10, offset: int = 0) -> List[Video]:
    return db.query(Video).order_by(Video.id.desc()).offset(offset).limit(limit).all()

def obter_video_por_id_youtube(db: Session, video_id_youtube: str):
    return db.query(Video).filter(Video.video_id_youtube == video_id_youtube).first()

def obter_comentarios_de_video(db: Session, video_id:int) -> list[str]:
    comentarios = db.query(Comentario.texto).filter(Comentario.video_id == video_id).all()
    return [c[0] for c in comentarios]

def deletar_video_por_id(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    if video:
        db.delete(video)
        db.commit()
        return True
    return False