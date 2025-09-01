from pydantic import BaseModel, Field
from typing import Optional


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
    id: int
    nombre: str
    email: str
    telefono: str
    cedula: str
    direccion: Optional[str] = None
    fecha_registro: Optional[str] = None

    class Config:
        from_attributes = True
