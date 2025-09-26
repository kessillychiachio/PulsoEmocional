from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    video_id_youtube = Column(String, unique=True, index=True)
    resumo = Column(Text, nullable=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)

    comentarios = relationship("Comentario", back_populates="video", cascade="all, delete-orphan")

class Comentario(Base):
    __tablename__ = "comentarios"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False)
    polaridade = Column(String, nullable=False)
    emocao = Column(String, nullable=True)
    video_id = Column(Integer, ForeignKey("videos.id"))

    video = relationship("Video", back_populates="comentarios")