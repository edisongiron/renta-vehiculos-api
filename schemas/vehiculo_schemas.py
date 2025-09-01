from pydantic import BaseModel, Field
from typing import Optional, List
from models.Vehiculo import TipoVehiculo, EstadoVehiculo


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
