from backend.database.db import engine, Base
from backend.models import Analise

Base.metadata.create_all(bind=engine)