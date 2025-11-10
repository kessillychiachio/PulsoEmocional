from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

engine = create_engine(
    "sqlite:///./data.db", 
    connect_args={"check_same_thread": False}, 
    poolclass=NullPool
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()