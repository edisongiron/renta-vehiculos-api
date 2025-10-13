from sqlalchemy import Table, Column, ForeignKey, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, Float
from database.db import meta
import uuid
from sqlalchemy.sql import func

vehiculo = Table(
    "vehiculo",
    meta,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("tipo", String(40)),
    Column("marca", String(100)),
    Column("modelo", String(100)),
    Column("anio", Integer),
    Column("placa", String(20), unique=True),
    Column("precio_por_dia", Float),
    Column("caracteristicas", String(255)),
    
    # Campos de auditoría
    Column("creado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("actualizado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("fecha_creacion", DateTime, default=func.now()),
    Column("fecha_actualizacion", DateTime, default=func.now(), onupdate=func.now()),
)
