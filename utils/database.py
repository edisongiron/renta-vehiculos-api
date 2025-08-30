from models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from typing import List
from datetime import datetime

# Base de datos simulada en memoria
vehiculos_db: List[Vehiculo] = [
    Vehiculo(
        id=1,
        tipo=TipoVehiculo.AUTO,
        marca="Toyota",
        modelo="Corolla",
        año=2022,
        placa="ABC123",
        precio_por_dia=50.0,
        estado=EstadoVehiculo.DISPONIBLE,
        caracteristicas="Automático, aire acondicionado, GPS"
    ),
    Vehiculo(
        id=2,
        tipo=TipoVehiculo.AUTO,
        marca="Honda",
        modelo="Civic",
        año=2021,
        placa="DEF456",
        precio_por_dia=45.0,
        estado=EstadoVehiculo.DISPONIBLE,
        caracteristicas="Manual, aire acondicionado"
    ),
    Vehiculo(
        id=3,
        tipo=TipoVehiculo.MOTO,
        marca="Yamaha",
        modelo="MT-07",
        año=2023,
        placa="GHI789",
        precio_por_dia=25.0,
        estado=EstadoVehiculo.DISPONIBLE,
        caracteristicas="600cc, deportiva"
    ),
    Vehiculo(
        id=4,
        tipo=TipoVehiculo.MOTO,
        marca="Honda",
        modelo="CB300R",
        año=2022,
        placa="JKL012",
        precio_por_dia=20.0,
        estado=EstadoVehiculo.ALQUILADO,
        caracteristicas="300cc, urbana"
    ),
    Vehiculo(
        id=5,
        tipo=TipoVehiculo.BICICLETA,
        marca="Trek",
        modelo="FX 3",
        año=2023,
        placa="BIC001",
        precio_por_dia=10.0,
        estado=EstadoVehiculo.DISPONIBLE,
        caracteristicas="Híbrida, 21 velocidades"
    ),
    Vehiculo(
        id=6,
        tipo=TipoVehiculo.BICICLETA,
        marca="Specialized",
        modelo="Rockhopper",
        año=2022,
        placa="BIC002",
        precio_por_dia=12.0,
        estado=EstadoVehiculo.DISPONIBLE,
        caracteristicas="Montañera, suspensión frontal"
    )
]

# Contadores para generar IDs únicos
next_vehiculo_id = 7
