from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.db import engine
from backend.models.base import Base
from backend.routes import video_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pulso Emocional - Análise de Sentimentos",
    description="Uma API para coletar, analisar e sumarizar comentários de vídeos do YouTube.",
    version="1.0.0",
)

origins = [
    "http://localhost:5173", 
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(video_routes.router)