from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EstadoAlquiler(int, Enum):
    ACTIVO = 1
    COMPLETADO = 2
    CANCELADO = 3


class Alquiler(BaseModel):
    id: Optional[str] = Field(None, description="ID único del alquiler")
    cliente_id: str = Field(..., description="ID del cliente")
    vehiculo_id: str = Field(..., description="ID del vehículo")
    fecha_inicio: str = Field(
        ..., description="Fecha de inicio del alquiler", examples=["2024-01-15"]
    )
    fecha_fin: str = Field(
        ..., description="Fecha de fin del alquiler", examples=["2024-01-20"]
    )
    dias_alquiler: int = Field(
        ..., description="Número de días de alquiler", examples=[5]
    )
    precio_total: float = Field(
        ..., description="Precio total del alquiler", examples=[250.0]
    )
    estado_id: int = Field(
        default=1, description="ID del estado del alquiler (1=activo, 2=completado, 3=cancelado)"
    )
    fecha_devolucion_real: Optional[str] = Field(
        None, description="Fecha real de devolución"
    )
    observaciones: Optional[str] = Field(None, description="Observaciones del alquiler")
    
    # Campos de auditoría
    creado_por: Optional[str] = Field(None, description="ID del usuario que creó el registro")
    actualizado_por: Optional[str] = Field(None, description="ID del usuario que actualizó el registro")
    fecha_creacion: Optional[datetime] = Field(None, description="Fecha de creación del registro")
    fecha_actualizacion: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        use_enum_values = True
        from_attributes = True


class AlquilerCreate(BaseModel):
    cliente_id: str = Field(..., description="ID del cliente")
    vehiculo_id: str = Field(..., description="ID del vehículo")
    fecha_inicio: str = Field(
        ...,
        description="Fecha de inicio del alquiler (YYYY-MM-DD)",
        examples=["2024-01-15"],
    )
    fecha_fin: str = Field(
        ...,
        description="Fecha de fin del alquiler (YYYY-MM-DD)",
        examples=["2024-01-20"],
    )
    observaciones: Optional[str] = Field(None, description="Observaciones del alquiler")


class AlquilerDevolucion(BaseModel):
    fecha_devolucion: str = Field(
        ..., description="Fecha de devolución (YYYY-MM-DD)", examples=["2024-01-20"]
    )
    observaciones: Optional[str] = Field(
        None, description="Observaciones de la devolución"
    )


class AlquilerResponse(BaseModel):
    id: str
    cliente_id: str
    vehiculo_id: str
    fecha_inicio: str
    fecha_fin: str
    dias_alquiler: int
    precio_total: float
    estado_id: int
    estado_nombre: Optional[str] = None  # Para mostrar el nombre del estado
    fecha_devolucion_real: Optional[str] = None
    observaciones: Optional[str] = None
    
    # Campos de auditoría (opcionales para respuesta)
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class AlquilerDetallado(BaseModel):
    id: str
    cliente_nombre: str
    cliente_email: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_placa: str
    vehiculo_tipo: str
    fecha_inicio: str
    fecha_fin: str
    dias_alquiler: int
    precio_total: float
    estado_id: int
    estado_nombre: Optional[str] = None
    fecha_devolucion_real: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        use_enum_values = True


class CalcularCosto(BaseModel):
    vehiculo_id: str = Field(..., description="ID del vehículo")
    fecha_inicio: str = Field(
        ..., description="Fecha de inicio (YYYY-MM-DD)", examples=["2024-01-15"]
    )
    fecha_fin: str = Field(
        ..., description="Fecha de fin (YYYY-MM-DD)", examples=["2024-01-20"]
    )


class CostoResponse(BaseModel):
    vehiculo_id: str
    precio_por_dia: float
    dias_alquiler: int
    precio_total: float
    descuento_aplicado: Optional[float] = None
    razon_descuento: Optional[str] = None
