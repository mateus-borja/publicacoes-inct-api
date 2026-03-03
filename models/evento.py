from pydantic import BaseModel
from datetime import date

class EventoModel(BaseModel):
    titulo: str
    resumo: str
    conteudo: str
    imagem: str
    dataInicio: date
    dataFim: date
    local: str
    laboratorio: str
    tags: list

class UpdateEventoModel(BaseModel):
    titulo: str = None
    resumo: str = None
    conteudo: str = None
    imagem: str = None
    dataInicio: date = None
    dataFim: date = None
    local: str = None
    laboratorio: str = None
    tags: list = None