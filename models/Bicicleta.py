from .Vehiculo import VehiculoCreate, VehiculoResponse, TipoVehiculo
from pydantic import Field, field_validator
from enum import Enum

class TipoBicicleta(str, Enum):
    MONTANA = "montana"
    RUTA = "ruta"
    HIBRIDA = "hibrida"
    ELECTRICA = "electrica"
    BMX = "bmx"
    URBANA = "urbana"

class BicicletaBase(VehiculoCreate):
    """Schema base para Bicicleta"""
    tipo_vehiculo: TipoVehiculo = Field(default=TipoVehiculo.BICICLETA, description="Tipo de vehículo (bicicleta)")
    tipo_bicicleta: TipoBicicleta = Field(..., description="Tipo de bicicleta")
    tiene_cambios: bool = Field(default=True, description="Si la bicicleta tiene cambios")
    numero_velocidades: int = Field(default=1, ge=1, le=30, description="Número de velocidades")
    
    @field_validator('tipo_vehiculo')
    def validate_tipo_vehiculo(cls, v_type):
        if v_type != TipoVehiculo.BICICLETA:
            raise ValueError('tipo_vehiculo debe ser "bicicleta" para la clase Bicicleta')
        
        return v_type

class BicicletaCreate(BicicletaBase):
    """Schema para crear una bicicleta (request)"""
    pass

class Bicicleta(VehiculoResponse):
    """Modelo completo de Bicicleta (response)"""
    tipo_vehiculo: TipoVehiculo = Field(default=TipoVehiculo.BICICLETA)
    tipo_bicicleta: TipoBicicleta
    tiene_cambios: bool
    numero_velocidades: int
