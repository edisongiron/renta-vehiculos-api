from pydantic import BaseModel, Field
from typing import Optional
from models.alquiler import EstadoAlquiler


class AlquilerCreate(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente", examples=[1])
    vehiculo_id: int = Field(..., description="ID del vehículo", examples=[1])
    fecha_inicio: str = Field(..., description="Fecha de inicio del alquiler (YYYY-MM-DD)", examples=["2024-01-15"])
    fecha_fin: str = Field(..., description="Fecha de fin del alquiler (YYYY-MM-DD)", examples=["2024-01-20"])
    observaciones: Optional[str] = Field(None, description="Observaciones del alquiler")


class AlquilerDevolucion(BaseModel):
    fecha_devolucion: str = Field(..., description="Fecha de devolución (YYYY-MM-DD)", examples=["2024-01-20"])
    observaciones: Optional[str] = Field(None, description="Observaciones de la devolución")


class AlquilerResponse(BaseModel):
    id: int
    cliente_id: int
    vehiculo_id: int
    fecha_inicio: str
    fecha_fin: str
    dias_alquiler: int
    precio_total: float
    estado: EstadoAlquiler
    fecha_devolucion_real: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class AlquilerDetallado(BaseModel):
    id: int
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
    estado: EstadoAlquiler
    fecha_devolucion_real: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        use_enum_values = True


class CalcularCosto(BaseModel):
    vehiculo_id: int = Field(..., description="ID del vehículo", examples=[1])
    fecha_inicio: str = Field(..., description="Fecha de inicio (YYYY-MM-DD)", examples=["2024-01-15"])
    fecha_fin: str = Field(..., description="Fecha de fin (YYYY-MM-DD)", examples=["2024-01-20"])


class CostoResponse(BaseModel):
    vehiculo_id: int
    precio_por_dia: float
    dias_alquiler: int
    precio_total: float
    descuento_aplicado: Optional[float] = None
    razon_descuento: Optional[str] = None
