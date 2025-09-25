from fastapi import FastAPI
from backend.database.db import engine
from backend.models.base import Base
from backend.routes import video_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Análise de Sentimentos em Vídeos do YouTube",
    description="Uma API para coletar, analisar e sumarizar comentários de vídeos.",
    version="1.0.0",
)

app.include_router(videos_routes.router)