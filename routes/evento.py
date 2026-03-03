from fastapi import APIRouter, Depends
from models.evento import EventoModel, UpdateEventoModel
from config.config import eventos_collection  
from serializers.serializers import DecodeEventos, DecodeEvento
from routes.auth import get_current_user, require_admin
import datetime
from bson import ObjectId

eventos_root = APIRouter() 

@eventos_root.post("/eventos")
def create_evento(evento: EventoModel, current_user: dict = Depends(get_current_user)):
    evento = dict(evento)
    current_date = datetime.date.today()
    evento["created_at"] = str(current_date)
    evento["created_by"] = current_user["id"]
    evento["created_by_name"] = current_user["nome"]

    res = eventos_collection.insert_one(evento)
    evento_id = str(res.inserted_id)

    return {
        "status": "ok",
        "message": "Evento criado com sucesso",
        "_id": evento_id
    }

# Pegando todos os eventos
@eventos_root.get("/eventos")
def get_eventos():
    res = eventos_collection.find()
    decoded_data = DecodeEventos(res)
    return {
        "status": "OK",
        "data": decoded_data
    }

# Pegando eventos futuros
@eventos_root.get("/eventos/futuros")
def get_eventos_futuros():
    current_date = datetime.date.today()
    res = eventos_collection.find({"dataInicio": {"$gte": current_date.isoformat()}})
    decoded_data = DecodeEventos(res)
    return {
        "status": "OK",
        "data": decoded_data
    }

# Pegando um evento específico pelo id
@eventos_root.get("/eventos/{_id}")
def get_evento(_id: str):
    res = eventos_collection.find_one({"_id": ObjectId(_id)})
    if not res:
        return {"status": "error", "message": "Evento não encontrado"}
    
    decoded_x = DecodeEvento(res)
    return {
        "status": "ok",
        "data": decoded_x
    }

@eventos_root.patch("/eventos/{_id}")
def update_evento(_id: str, evento: UpdateEventoModel, current_user: dict = Depends(get_current_user)):
    req = dict(evento.model_dump(exclude_unset=True))
    req["updated_by"] = current_user["id"]
    req["updated_at"] = str(datetime.datetime.now())
    
    result = eventos_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": req})
    if result:
        return {"status": "ok", "message": "Evento atualizado com sucesso"}
    return {"status": "error", "message": "Evento não encontrado"}

@eventos_root.delete("/eventos/{_id}")
def delete_evento(_id: str, admin_user: dict = Depends(require_admin)):
    result = eventos_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count:
        return {"status": "ok", "message": "Evento removido com sucesso"}
    return {"status": "error", "message": "Evento não encontrado"}

@eventos_root.delete("/eventos")
def delete_all_eventos(admin_user: dict = Depends(require_admin)):
    result = eventos_collection.delete_many({})
    return {
        "status": "ok",
        "message": f"Todos os {result.deleted_count} eventos foram deletados com sucesso"
    }