from fastapi import APIRouter
from models.publicacao import PublicacaoModel , UpdatePublicacaoModel
from config.config import publications_collection  
from serializers.site import DecodePublicacoes, DecodePublicacao
import datetime
from bson import ObjectId
publicacoes_root = APIRouter() 

@publicacoes_root.post("/new/publicacao")
def create_publicacao(publicacao: PublicacaoModel):
    publicacao = dict(publicacao)
    current_date = datetime.date.today()
    publicacao["date"] = str(current_date)

    res = publications_collection.insert_one(publicacao)
    publicacao_id = str(res.inserted_id)

    return {
        "status": "ok",
        "message": "Publicação criada com sucesso",
        "_id": publicacao_id
    }

#pegando todas as publicações
@publicacoes_root.get("/all/publicacoes")
def get_publicacoes():
    res = publications_collection.find()
    decoded_data = DecodePublicacoes(res)
    return {
        "status": "OK",
        "data": decoded_data
    }


#pegando uma publicação específica pelo id
@publicacoes_root.get("/publicacao/{_id}")
def get_publicacao(_id: str):

    res = publications_collection.find_one({"_id": ObjectId(_id)})
    decoded_x = DecodePublicacao(res)

    return {
        "status": "ok",
        "data": decoded_x
    }

@publicacoes_root.patch("/update/{_id}")
def update_publicacao(_id: str, publicacao: UpdatePublicacaoModel):
    req = dict(publicacao.model_dump(exclude_unset=True))
    publications_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": req})

    return {
        "status": "ok",
        "message": "Publicação atualizada com sucesso"
    }

@publicacoes_root.delete("/delete/{_id}")
def delete_publicacao(_id: str):
    publications_collection.find_one_and_delete({"_id": ObjectId(_id)})

    return {
        "status": "ok",
        "message": "Publicação deletada com sucesso"
    }

@publicacoes_root.delete("/delete/all/publicacoes")
def delete_all_publicacoes():
    publications_collection.delete_many({})

    return {
        "status": "ok",
        "message": "Todas as publicações foram deletadas com sucesso"
    }