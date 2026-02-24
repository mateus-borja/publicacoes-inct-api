from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    email: EmailStr
    nome: str
    senha: str
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    id: str
    email: str
    nome: str
    role: str

class UpdateUserModel(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    role: Optional[str] = None