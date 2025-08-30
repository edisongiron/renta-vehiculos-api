from pydantic import BaseModel

class Vehiculo(BaseModel):
    id: int
    marca: str
    modelo: str
    anio: int
    color: str
    precio_por_dia: float
    disponible: bool


