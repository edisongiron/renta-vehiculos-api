from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from database.db import meta

estado_alquiler = Table(
    "estado_alquiler",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(20), unique=True, nullable=False),
)
