from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class TipoVehiculo(str, Enum):
    AUTO = "auto"
    MOTO = "moto"
    BICICLETA = "bicicleta"


class EstadoVehiculo(str, Enum):
    DISPONIBLE = "disponible"
    ALQUILADO = "alquilado"
    MANTENIMIENTO = "mantenimiento"


class VehiculoBase(BaseModel):
    """Esquema base para vehículos"""
    tipo: TipoVehiculo = Field(..., description="Tipo de vehículo")
    marca: str = Field(..., description="Marca del vehículo", examples=["Toyota"])
    modelo: str = Field(..., description="Modelo del vehículo", examples=["Corolla"])
    año: int = Field(..., description="Año del vehículo", examples=[2022])
    placa: str = Field(..., description="Placa del vehículo", examples=["ABC123"])
    precio_por_dia: float = Field(..., description="Precio de alquiler por día", examples=[50.0])
    estado: EstadoVehiculo = Field(default=EstadoVehiculo.DISPONIBLE, description="Estado actual del vehículo")
    caracteristicas: Optional[str] = Field(None, description="Características adicionales del vehículo")

    class Config:
        use_enum_values = True


class VehiculoCreate(VehiculoBase):
    """Esquema para crear un vehículo (request)"""
    pass


class VehiculoResponse(VehiculoBase):
    """Esquema de respuesta para vehículo"""
    id: int = Field(..., description="ID único del vehículo", examples=[1])


class Vehiculo(VehiculoResponse):
    """Modelo completo de vehículo (mantener para compatibilidad)"""
    pass

class VehiculoCreate(BaseModel):
    tipo: TipoVehiculo = Field(..., description="Tipo de vehículo")
    marca: str = Field(..., description="Marca del vehículo", examples=["Toyota"])
    modelo: str = Field(..., description="Modelo del vehículo", examples=["Corolla"])
    año: int = Field(..., description="Año del vehículo", examples=[2022])
    placa: str = Field(..., description="Placa del vehículo", examples=["ABC123"])
    precio_por_dia: float = Field(..., description="Precio de alquiler por día", examples=[50.0])
    caracteristicas: Optional[str] = Field(None, description="Características adicionales del vehículo")


class VehiculoUpdate(BaseModel):
    marca: Optional[str] = Field(None, description="Marca del vehículo")
    modelo: Optional[str] = Field(None, description="Modelo del vehículo")
    año: Optional[int] = Field(None, description="Año del vehículo")
    precio_por_dia: Optional[float] = Field(None, description="Precio de alquiler por día")
    estado: Optional[EstadoVehiculo] = Field(None, description="Estado del vehículo")
    caracteristicas: Optional[str] = Field(None, description="Características adicionales")


class VehiculoResponse(BaseModel):
    id: int
    tipo: TipoVehiculo
    marca: str
    modelo: str
    año: int
    placa: str
    precio_por_dia: float
    estado: EstadoVehiculo
    caracteristicas: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class VehiculoDisponibilidad(BaseModel):
    vehiculo_id: int
    disponible: bool
    razon: Optional[str] = None