# app/schemas/user.py

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Nuevo esquema para la respuesta de registro
class UserResponse(BaseModel):
    message: str
    user: User
