from backend.database.db import engine, Base

Base.metadata.create_all(bind=engine)