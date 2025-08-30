from models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from models.cliente import Cliente
from models.alquiler import Alquiler, EstadoAlquiler
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

clientes_db: List[Cliente] = [
    Cliente(
        id=1,
        nombre="Juan Pérez",
        email="juan.perez@gmail.com",
        telefono="+57 300 123 4567",
        cedula="12345678",
        direccion="Calle 123 #45-67, Bogotá",
        fecha_registro="2024-01-01"
    ),
    Cliente(
        id=2,
        nombre="María García",
        email="maria.garcia@gmail.com",
        telefono="+57 301 234 5678",
        cedula="87654321",
        direccion="Carrera 45 #12-34, Medellín",
        fecha_registro="2024-01-15"
    ),
    Cliente(
        id=3,
        nombre="Carlos Rodríguez",
        email="carlos.rodriguez@gmail.com",
        telefono="+57 302 345 6789",
        cedula="11223344",
        direccion="Avenida 68 #23-45, Cali",
        fecha_registro="2024-02-01"
    )
]

alquileres_db: List[Alquiler] = [
    Alquiler(
        id=1,
        cliente_id=2,
        vehiculo_id=4,
        fecha_inicio="2024-08-25",
        fecha_fin="2024-08-30",
        dias_alquiler=5,
        precio_total=100.0,
        estado=EstadoAlquiler.ACTIVO,
        observaciones="Cliente experimentado en motos"
    )
]

# Contadores para generar IDs únicos
next_vehiculo_id = 7
next_cliente_id = 4
next_alquiler_id = 2
