from pydantic import BaseModel
from datetime import date

class NoticiaModel(BaseModel):
    titulo: str
    resumo: str
    conteudo: str
    imagem: str
    data: date
    laboratorio: str
    tags: list
    link: str
    publicado: bool

class UpdateNoticiaModel(BaseModel):
    titulo: str = None
    resumo: str = None
    conteudo: str = None
    imagem: str = None
    data: date = None
    laboratorio: str = None
    tags: list = None
    link: str = None
    publicado: bool = None