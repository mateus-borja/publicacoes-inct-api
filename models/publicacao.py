from pydantic import BaseModel

class PublicacaoModel(BaseModel):
    titulo:str
    autores:str
    ano:int
    link:str
    post_img:str
    tags : list

class UpdatePublicacaoModel(BaseModel):
    titulo:str = None
    autores:str = None
    ano:int = None
    link:str = None
    post_img:str = None
    tags : list = None