from fastapi import APIRouter, Depends
from controllers.auth import Auth
from models.auth import UserLogin, UserRegister, UserResponse, TokenResponse
from utils.auth_utils import get_current_user
from database.db import get_db
from sqlalchemy.orm import Session
from typing import Dict

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# POST -> /auth/login
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login de usuario",
    description="Autentica un usuario y devuelve un token JWT"
)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return Auth.login(user_data, db)

# POST -> /auth/register
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Registro de usuario",
    description="Registra un nuevo usuario en el sistema"
)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    return Auth.register(user_data, db)

# GET -> /auth/me
@router.get(
    "/me",
    response_model=Dict,
    summary="Obtener usuario actual",
    description="Obtiene la información del usuario autenticado actual"
)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

# GET -> /auth/verify
@router.get(
    "/verify",
    response_model=Dict,
    summary="Verificar token",
    description="Verifica si el token JWT es válido"
)
def verify_token(current_user: dict = Depends(get_current_user)):
    return {"valid": True, "user_id": current_user["id"], "username": current_user["username"]}
