from pydantic import BaseModel, model_validator
from typing import Literal

class Questao(BaseModel):
    enunciado: str
    alternativas: list  # [{ "texto": str, "correta": bool }]
    explicacao: str = None

class Conteudo(BaseModel):
    tipo: Literal["video", "pdf", "questoes"]
    url: str = None          # YouTube embed url ou PDF url
    questoes: list[Questao] = None

    @model_validator(mode="after")
    def valida_campos(self):
        if self.tipo in ("video", "pdf") and not self.url:
            raise ValueError(f"'url' é obrigatório quando tipo é '{self.tipo}'")
        if self.tipo == "questoes" and not self.questoes:
            raise ValueError("'questoes' é obrigatório quando tipo é 'questoes'")
        return self

class ModuloModel(BaseModel):
    titulo: str
    ordem: int
    conteudos: list[Conteudo]

class UpdateModuloModel(BaseModel):
    titulo: str = None
    ordem: int = None
    conteudos: list[Conteudo] = None

class CursoModel(BaseModel):
    titulo: str
    descricao: str
    imagem: str
    tags: list = []
    publicado: bool = False

class UpdateCursoModel(BaseModel):
    titulo: str = None
    descricao: str = None
    imagem: str = None
    tags: list = None
    publicado: bool = None
