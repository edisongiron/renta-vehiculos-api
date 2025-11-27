from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Cliente(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[str] = Field(..., description="UUID único del cliente", examples=[""])
    nombre: str = Field(..., description="Nombre completo del cliente", examples=["Juan Pérez"])
    email: str = Field(..., description="Correo electrónico del cliente", examples=["juan.perez@gmail.com"])
    telefono: str = Field(..., description="Número de teléfono", examples=["+57 300 123 4567"])
    cedula: str = Field(..., description="Número de identificación", examples=["12345678"])
    direccion: Optional[str] = Field(None, description="Dirección del cliente")
    fecha_registro: Optional[str] = Field(None, description="Fecha de registro del cliente")

class ClienteCreate(BaseModel):
    nombre: str = Field(..., description="Nombre completo del cliente", examples=["Juan Pérez"])
    email: str = Field(..., description="Correo electrónico del cliente", examples=["juan.perez@gmail.com"])
    telefono: str = Field(..., description="Número de teléfono", examples=["+57 300 123 4567"])
    cedula: str = Field(..., description="Número de identificación", examples=["12345678"])
    direccion: Optional[str] = Field(None, description="Dirección del cliente")


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre completo del cliente")
    email: Optional[str] = Field(None, description="Correo electrónico del cliente")
    telefono: Optional[str] = Field(None, description="Número de teléfono")
    direccion: Optional[str] = Field(None, description="Dirección del cliente")


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[str] = None
    nombre: str
    email: str
    telefono: str
    cedula: str
    direccion: Optional[str] = None
    fecha_registro: Optional[str] = None
