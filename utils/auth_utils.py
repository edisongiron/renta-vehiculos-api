from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from database.db import get_db
from sqlalchemy.orm import Session
from schemas.auth_usuarios import auth_usuarios

# Configuración
SECRET_KEY = "tu_clave_secreta_muy_segura_aqui_cambiarla_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurar el contexto para hashear passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Obtiene el usuario actual a partir del token JWT"""
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")
    
    # Buscar el usuario en la base de datos
    query = select(auth_usuarios).where(auth_usuarios.c.id == user_id)
    result = db.execute(query).first()
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    
    if not result.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )
    
    return {
        "id": result.id,
        "username": result.username,
        "email": result.email,
        "nombre_completo": result.nombre_completo,
        "rol_id": result.rol_id,
        "activo": result.activo
    }

def authenticate_user(username: str, password: str, db: Session):
    """Autentica un usuario con username y password"""
    query = select(auth_usuarios).where(auth_usuarios.c.username == username)
    result = db.execute(query).first()
    
    if not result:
        return False
    
    if not verify_password(password, result.password_hash):
        return False
    
    if not result.activo:
        return False
    
    return {
        "id": result.id,
        "username": result.username,
        "email": result.email,
        "nombre_completo": result.nombre_completo,
        "rol_id": result.rol_id,
        "activo": result.activo
    }
