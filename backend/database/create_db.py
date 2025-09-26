from backend.database.db import engine, Base
from backend.models.video_models import Video, Comentario

Base.metadata.create_all(bind=engine)