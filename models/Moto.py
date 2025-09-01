from .Vehiculo import VehiculoCreate, VehiculoResponse, TipoVehiculo
from pydantic import Field, field_validator
from enum import Enum

class TipoMoto(str, Enum):
    DEPORTIVA = "deportiva"
    CRUISER = "cruiser"
    TOURING = "touring"
    SCOOTER = "scooter"
    ELECTRICA = "electrica"

class MotoBase(VehiculoCreate):
    """Schema base para Moto"""
    tipo_vehiculo: TipoVehiculo = Field(default=TipoVehiculo.MOTO, description="Tipo de vehículo (moto)")
    tipo_moto: TipoMoto = Field(..., description="Tipo de moto")
    cilindraje: int = Field(..., ge=50, le=2000, description="Cilindraje en cc")
    
    @field_validator('tipo_vehiculo')
    @classmethod
    def validate_tipo_vehiculo(cls, v):
        if v != TipoVehiculo.MOTO:
            raise ValueError('tipo_vehiculo debe ser "moto" para la clase Moto')
        return v

class MotoCreate(MotoBase):
    """Schema para crear una moto (request)"""
    pass

class Moto(VehiculoResponse):
    """Modelo completo de Moto (response)"""
    tipo_vehiculo: TipoVehiculo = Field(default=TipoVehiculo.MOTO)
    tipo_moto: TipoMoto
    cilindraje: int
