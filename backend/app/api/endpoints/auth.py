# app/api/endpoints/auth.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas
from app.schemas.user import UserResponse  # Importa UserResponse aquí
from app.core import security
from app.core.config import settings
from app.api import deps
from app.crud import crud_user

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud_user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/signup", response_model=UserResponse)
def signup(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    # Verificar si el nombre de usuario ya está en uso
    existing_user = crud_user.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    # Verificar si el correo electrónico ya está en uso
    existing_email = crud_user.get_by_email(db, email=user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    # Crear el nuevo usuario
    user = crud_user.create(db, obj_in=user_in)
    
    # Retornar el usuario creado con un mensaje de éxito
    return {"message": "Registro exitoso", "user": user}
