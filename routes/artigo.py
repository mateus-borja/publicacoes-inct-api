from fastapi import APIRouter
from models.artigo import ArtigoModel , UpdateArtigoModel
from config.config import publications_collection  
from serializers.site import DecodeArtigos, DecodeArtigo
import datetime
from bson import ObjectId
artigos_root = APIRouter() 

@artigos_root.post("/artigos")
def create_artigo(artigo: ArtigoModel):
    artigo = dict(artigo)
    current_date = datetime.date.today()
    artigo["date"] = str(current_date)

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
def update_artigo(_id: str, artigo: UpdateArtigoModel):
    req = dict(artigo.model_dump(exclude_unset=True))
    publications_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": req})

    return {
        "status": "ok",
        "message": "Artigo atualizado com sucesso"
    }

@artigos_root.delete("/artigos/{_id}")
def delete_artigo(_id: str):
    publications_collection.find_one_and_delete({"_id": ObjectId(_id)})

    return {
        "status": "ok",
        "message": "Artigo deletado com sucesso"
    }

@artigos_root.delete("/artigos")
def delete_all_artigos():
    publications_collection.delete_many({})

    return {
        "status": "ok",
        "message": "Todos os artigos foram deletados com sucesso"
    }