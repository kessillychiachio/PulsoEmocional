from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ComentarioOut(BaseModel):
    id: int
    texto: str
    polaridade: str
    emocao: Optional[str] = None

    class Config:
        from_attributes = True
        
class VideoOut(BaseModel):
    id: int
    video_id_youtube: str
    titulo: Optional[str] = None
    resumo: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
        
class VideoDetalheOut(VideoOut):
    comentarios: List[ComentarioOut] = []