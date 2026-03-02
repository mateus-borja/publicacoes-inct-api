from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserModel, UserLogin, UserResponse
from config.config import users_collection
from utils.jwt_handler import create_access_token, verify_token
from passlib.context import CryptContext
from bson import ObjectId

auth_router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@auth_router.post("/register")
def register(user: UserModel):
    # Verificar se usuário já existe
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Hash da senha
    user_dict = user.model_dump()
    user_dict["senha"] = hash_password(user.senha)
    
    # Inserir no MongoDB
    result = users_collection.insert_one(user_dict)
    
    return {"status": "ok", "message": "Usuário criado com sucesso", "user_id": str(result.inserted_id)}

@auth_router.post("/login")
def login(user_credentials: UserLogin):
    user = users_collection.find_one({"email": user_credentials.email})
    
    if not user or not verify_password(user_credentials.senha, user["senha"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Criar token JWT
    access_token = create_access_token(
        data={"user_id": str(user["_id"]), "email": user["email"], "role": user["role"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "nome": user["nome"],
            "role": user["role"]
        }
    }

# Middleware para verificar token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "nome": user["nome"],
        "role": user["role"]
    }

# Middleware para admin apenas
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado - Admin necessário")
    return current_user

@auth_router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"status": "ok", "user": current_user}