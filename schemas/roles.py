from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from database.db import meta

roles = Table(
    "roles",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50), unique=True, nullable=False),
    Column("descripcion", String(200))
)
