from fastapi import APIRouter, Depends
from models.noticia import NoticiaModel, UpdateNoticiaModel
from config.config import noticias_collection  
from serializers.serializers import DecodeNoticias, DecodeNoticia
from routes.auth import get_current_user, require_admin
import datetime
from bson import ObjectId

noticias_root = APIRouter() 

@noticias_root.post("/noticias")
def create_noticia(noticia: NoticiaModel, current_user: dict = Depends(get_current_user)):
    noticia = dict(noticia)
    current_date = datetime.date.today()
    noticia["created_at"] = str(current_date)
    noticia["created_by"] = current_user["id"]
    noticia["created_by_name"] = current_user["nome"]

    res = noticias_collection.insert_one(noticia)
    noticia_id = str(res.inserted_id)

    return {
        "status": "ok",
        "message": "Notícia criada com sucesso",
        "_id": noticia_id
    }

# Pegando todas as notícias
@noticias_root.get("/noticias")
def get_noticias():
    res = noticias_collection.find()
    decoded_data = DecodeNoticias(res)
    return {
        "status": "OK",
        "data": decoded_data
    }

# Pegando notícias publicadas apenas
@noticias_root.get("/noticias/publicadas")
def get_noticias_publicadas():
    res = noticias_collection.find({"publicado": True})
    decoded_data = DecodeNoticias(res)
    return {
        "status": "OK",
        "data": decoded_data
    }

# Pegando uma notícia específica pelo id
@noticias_root.get("/noticias/{_id}")
def get_noticia(_id: str):
    res = noticias_collection.find_one({"_id": ObjectId(_id)})
    if not res:
        return {"status": "error", "message": "Notícia não encontrada"}
    
    decoded_x = DecodeNoticia(res)
    return {
        "status": "ok",
        "data": decoded_x
    }

@noticias_root.patch("/noticias/{_id}")
def update_noticia(_id: str, noticia: UpdateNoticiaModel, current_user: dict = Depends(get_current_user)):
    req = dict(noticia.model_dump(exclude_unset=True))
    req["updated_by"] = current_user["id"]
    req["updated_at"] = str(datetime.datetime.now())
    
    result = noticias_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": req})
    if result:
        return {"status": "ok", "message": "Notícia atualizada com sucesso"}
    return {"status": "error", "message": "Notícia não encontrada"}

@noticias_root.delete("/noticias/{_id}")
def delete_noticia(_id: str, admin_user: dict = Depends(require_admin)):
    result = noticias_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count:
        return {"status": "ok", "message": "Notícia removida com sucesso"}
    return {"status": "error", "message": "Notícia não encontrada"}

@noticias_root.delete("/noticias")
def delete_all_noticias(admin_user: dict = Depends(require_admin)):
    result = noticias_collection.delete_many({})
    return {
        "status": "ok",
        "message": f"Todas as {result.deleted_count} notícias foram deletadas com sucesso"
    }