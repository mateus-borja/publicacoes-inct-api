from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.curso import CursoModel, UpdateCursoModel, ModuloModel, UpdateModuloModel
from config.config import cursos_collection
from serializers.serializers import DecodeCursos, DecodeCurso
from routes.auth import get_current_user, require_admin
import datetime
from bson import ObjectId
import uuid

cursos_root = APIRouter()


# ── Cursos ──────────────────────────────────────────────────────────────────

@cursos_root.post("/cursos")
def create_curso(curso: CursoModel, current_user: dict = Depends(get_current_user)):
    doc = curso.model_dump()
    doc["modulos"] = []
    doc["created_at"] = str(datetime.date.today())
    doc["created_by"] = current_user["id"]
    doc["created_by_name"] = current_user["nome"]

    res = cursos_collection.insert_one(doc)
    return {
        "status": "ok",
        "message": "Curso criado com sucesso",
        "_id": str(res.inserted_id)
    }


@cursos_root.get("/cursos")
def get_cursos():
    res = cursos_collection.find()
    return {
        "status": "ok",
        "data": DecodeCursos(res)
    }


@cursos_root.get("/cursos/publicados")
def get_cursos_publicados():
    res = cursos_collection.find({"publicado": True})
    return {
        "status": "ok",
        "data": DecodeCursos(res)
    }


@cursos_root.get("/cursos/{_id}")
def get_curso(_id: str):
    res = cursos_collection.find_one({"_id": ObjectId(_id)})
    if not res:
        return {"status": "error", "message": "Curso não encontrado"}
    return {
        "status": "ok",
        "data": DecodeCurso(res)
    }


@cursos_root.patch("/cursos/{_id}")
def update_curso(_id: str, curso: UpdateCursoModel, current_user: dict = Depends(get_current_user)):
    req = curso.model_dump(exclude_unset=True)
    req["updated_by"] = current_user["id"]
    req["updated_at"] = str(datetime.datetime.now())

    result = cursos_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": req})
    if result:
        return {"status": "ok", "message": "Curso atualizado com sucesso"}
    return {"status": "error", "message": "Curso não encontrado"}


@cursos_root.delete("/cursos/{_id}")
def delete_curso(_id: str, admin_user: dict = Depends(require_admin)):
    result = cursos_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count:
        return {"status": "ok", "message": "Curso removido com sucesso"}
    return {"status": "error", "message": "Curso não encontrado"}


# ── Módulos ──────────────────────────────────────────────────────────────────

@cursos_root.post("/cursos/{_id}/modulos")
def add_modulo(_id: str, modulo: ModuloModel, current_user: dict = Depends(get_current_user)):
    doc = modulo.model_dump()
    doc["id"] = str(uuid.uuid4())

    result = cursos_collection.find_one_and_update(
        {"_id": ObjectId(_id)},
        {"$push": {"modulos": doc}}
    )
    if result:
        return {"status": "ok", "message": "Módulo adicionado com sucesso", "modulo_id": doc["id"]}
    return {"status": "error", "message": "Curso não encontrado"}


class OrdemItem(BaseModel):
    modulo_id: str
    ordem: int

@cursos_root.patch("/cursos/{_id}/modulos/reordenar")
def reordenar_modulos(_id: str, nova_ordem: list[OrdemItem], current_user: dict = Depends(get_current_user)):
    curso = cursos_collection.find_one({"_id": ObjectId(_id)})
    if not curso:
        return {"status": "error", "message": "Curso não encontrado"}

    ordem_map = {item.modulo_id: item.ordem for item in nova_ordem}
    modulos = curso.get("modulos", [])

    ids_enviados = set(ordem_map.keys())
    ids_existentes = {m["id"] for m in modulos}
    if ids_enviados != ids_existentes:
        raise HTTPException(status_code=400, detail="A lista deve conter todos os módulos do curso")

    for modulo in modulos:
        modulo["ordem"] = ordem_map[modulo["id"]]

    cursos_collection.update_one(
        {"_id": ObjectId(_id)},
        {"$set": {"modulos": modulos}}
    )
    return {"status": "ok", "message": "Módulos reordenados com sucesso"}


@cursos_root.patch("/cursos/{_id}/modulos/{modulo_id}")
def update_modulo(_id: str, modulo_id: str, modulo: UpdateModuloModel, current_user: dict = Depends(get_current_user)):
    req = modulo.model_dump(exclude_unset=True)
    update_fields = {f"modulos.$.{k}": v for k, v in req.items()}

    result = cursos_collection.find_one_and_update(
        {"_id": ObjectId(_id), "modulos.id": modulo_id},
        {"$set": update_fields}
    )
    if result:
        return {"status": "ok", "message": "Módulo atualizado com sucesso"}
    return {"status": "error", "message": "Curso ou módulo não encontrado"}


@cursos_root.delete("/cursos/{_id}/modulos/{modulo_id}")
def delete_modulo(_id: str, modulo_id: str, current_user: dict = Depends(get_current_user)):
    result = cursos_collection.find_one_and_update(
        {"_id": ObjectId(_id)},
        {"$pull": {"modulos": {"id": modulo_id}}}
    )
    if result:
        return {"status": "ok", "message": "Módulo removido com sucesso"}
    return {"status": "error", "message": "Curso ou módulo não encontrado"}
