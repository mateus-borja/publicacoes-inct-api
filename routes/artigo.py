from fastapi import APIRouter, Depends
from models.artigo import ArtigoModel , UpdateArtigoModel
from config.config import publications_collection  
from serializers.serializers import DecodeArtigos, DecodeArtigo
from routes.auth import get_current_user, require_admin
import datetime
from bson import ObjectId
artigos_root = APIRouter() 

@artigos_root.post("/artigos")
def create_artigo(artigo: ArtigoModel, current_user: dict = Depends(get_current_user)):
    artigo = dict(artigo)
    current_date = datetime.date.today()
    artigo["date"] = str(current_date)
    artigo["created_by"] = current_user["id"]
    artigo["created_by_name"] = current_user["nome"]

    res = publications_collection.insert_one(artigo)
    artigo_id = str(res.inserted_id)

    return {
        "status": "ok",
        "message": "Artigo criado com sucesso",
        "_id": artigo_id
    }

#pegando todos os artigos
@artigos_root.get("/artigos")
def get_artigos():
    res = publications_collection.find()
    decoded_data = DecodeArtigos(res)
    return {
        "status": "OK",
        "data": decoded_data
    }


#pegando um artigo específico pelo id
@artigos_root.get("/artigos/{_id}")
def get_artigo(_id: str):

    res = publications_collection.find_one({"_id": ObjectId(_id)})
    decoded_x = DecodeArtigo(res)

    return {
        "status": "ok",
        "data": decoded_x
    }

@artigos_root.patch("/artigos/{_id}")
def update_artigo(_id: str, artigo: UpdateArtigoModel, current_user: dict = Depends(get_current_user)):
    req = dict(artigo.model_dump(exclude_unset=True))
    req["updated_by"] = current_user["id"]
    req["updated_at"] = str(datetime.datetime.now())
    
    result = publications_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": req})
    if result:
        return {"status": "ok", "message": "Artigo atualizado com sucesso"}
    return {"status": "error", "message": "Artigo não encontrado"}

@artigos_root.delete("/artigos/{_id}")
def delete_artigo(_id: str, admin_user: dict = Depends(require_admin)):
    result = publications_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count:
        return {"status": "ok", "message": "Artigo removido com sucesso"}
    return {"status": "error", "message": "Artigo não encontrado"}

@artigos_root.delete("/artigos")
def delete_all_artigos(admin_user: dict = Depends(require_admin)):
    result = publications_collection.delete_many({})
    return {
        "status": "ok",
        "message": f"Todos os {result.deleted_count} artigos foram deletados com sucesso"
    }