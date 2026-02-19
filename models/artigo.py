from pydantic import BaseModel

class ArtigoModel(BaseModel):
    titulo:str
    autores:str
    ano:int
    link:str
    post_img:str
    tags : list

class UpdateArtigoModel(BaseModel):
    titulo:str = None
    autores:str = None
    ano:int = None
    link:str = None
    post_img:str = None
    tags : list = None