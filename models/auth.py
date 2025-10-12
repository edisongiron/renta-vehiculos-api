from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    username: str = Field(..., description="Nombre de usuario", min_length=3, max_length=50)
    password: str = Field(..., description="Contraseña", min_length=6)

class UserRegister(BaseModel):
    username: str = Field(..., description="Nombre de usuario", min_length=3, max_length=50)
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña", min_length=6)
    nombre_completo: Optional[str] = Field(None, description="Nombre completo del usuario", max_length=100)
    rol_id: Optional[int] = Field(2, description="ID del rol (default: usuario regular)")

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    nombre_completo: Optional[str]
    activo: bool
    rol_id: int
    fecha_creacion: Optional[datetime]
    ultimo_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None
    rol_id: Optional[int] = None

class PasswordChange(BaseModel):
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., description="Nueva contraseña", min_length=6)
