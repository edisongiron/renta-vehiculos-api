from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EstadoAlquiler(str, Enum):
    ACTIVO = "activo"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class Alquiler(BaseModel):
    id: int = Field(..., description="ID único del alquiler", examples=[1])
    cliente_id: int = Field(..., description="ID del cliente", examples=[1])
    vehiculo_id: int = Field(..., description="ID del vehículo", examples=[1])
    fecha_inicio: str = Field(..., description="Fecha de inicio del alquiler", examples=["2024-01-15"])
    fecha_fin: str = Field(..., description="Fecha de fin del alquiler", examples=["2024-01-20"])
    dias_alquiler: int = Field(..., description="Número de días de alquiler", examples=[5])
    precio_total: float = Field(..., description="Precio total del alquiler", examples=[250.0])
    estado: EstadoAlquiler = Field(default=EstadoAlquiler.ACTIVO, description="Estado del alquiler")
    fecha_devolucion_real: Optional[str] = Field(None, description="Fecha real de devolución")
    observaciones: Optional[str] = Field(None, description="Observaciones del alquiler")

    class Config:
        use_enum_values = True
        from_attributes = True
