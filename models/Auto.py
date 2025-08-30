from .vehiculo import VehiculoCreate, VehiculoResponse, TipoVehiculo
from pydantic import Field, field_validator
from enum import Enum


class TipoAuto(str, Enum):
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    COUPE = "coupe"
    CONVERTIBLE = "convertible"
    PICKUP = "pickup"

class AutoCreate(VehiculoCreate):
    """Schema para crear un auto"""
    tipo_vehiculo: TipoVehiculo = Field(default=TipoVehiculo.AUTO, description="Tipo de vehículo (auto)")
    tipo_auto: TipoAuto = Field(..., description="Tipo de auto")
    
    @field_validator('tipo_vehiculo')
    @classmethod
    def validate_tipo_vehiculo(cls, v):
        if v != TipoVehiculo.AUTO:
            raise ValueError('tipo_vehiculo debe ser "auto" para la clase Auto')
        return v

class Auto(VehiculoResponse):
    """Modelo completo de Auto"""
    tipo_vehiculo: TipoVehiculo = Field(default=TipoVehiculo.AUTO)
    tipo_auto: TipoAuto
