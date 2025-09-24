from sqlalchemy import Column, Integer, String, DateTime, Float, func
from db import Base

class Analise(Base):
    __tablename__ = "analises"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, nullable=False)
    polaridade = Column(String, nullable=False)
    origem = Column(String, nullable=False)
    confianca = Column(Float, nullable=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)