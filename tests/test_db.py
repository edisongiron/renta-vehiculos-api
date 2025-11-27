import pytest
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, insert, update, delete, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    meta = MetaData()
    
    cliente = Table(
        "cliente",
        meta,
        Column("id", String(36), primary_key=True),
        Column("nombre", String(100)),
        Column("email", String(100), unique=True),
        Column("cedula", String(20), unique=True),
        Column("telefono", String(50)),
        Column("direccion", String(150)),
        Column("fecha_registro", String(20))
    )
    
    vehiculo = Table(
        "vehiculo",
        meta,
        Column("id", String(36), primary_key=True),
        Column("tipo", String(50)),
        Column("marca", String(100)),
        Column("modelo", String(100)),
        Column("placa", String(50), unique=True),
        Column("precio_por_dia", Float),
        Column("estado", String(50)),
        Column("caracteristicas", String(500))
    )
    
    meta.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    session.tables = {"cliente": cliente, "vehiculo": vehiculo}
    return session


class TestClienteDatabase:
    def test_insert_cliente(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id = str(uuid.uuid4())
        stmt = insert(cliente_table).values(
            id=cliente_id,
            nombre="Juan Pérez",
            email="juan@test.com",
            cedula=12345678,
            telefono="+57 300 123 4567",
            fecha_registro="2024-01-01"
        )
        test_db.execute(stmt)
        test_db.commit()
        
        query = select(cliente_table).where(cliente_table.c.id == cliente_id)
        result = test_db.execute(query).fetchone()
        assert result is not None

    def test_cliente_unique_email(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id_1 = str(uuid.uuid4())
        cliente_id_2 = str(uuid.uuid4())
        
        stmt1 = insert(cliente_table).values(
            id=cliente_id_1, nombre="Juan", email="same@test.com", cedula="111", telefono="123"
        )
        test_db.execute(stmt1)
        test_db.commit()
        
        with pytest.raises(Exception):
            stmt2 = insert(cliente_table).values(
                id=cliente_id_2, nombre="Carlos", email="same@test.com", cedula="222", telefono="456"
            )
            test_db.execute(stmt2)
            test_db.commit()

    def test_cliente_unique_cedula(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id_1 = str(uuid.uuid4())
        cliente_id_2 = str(uuid.uuid4())
        
        stmt1 = insert(cliente_table).values(
            id=cliente_id_1, nombre="Juan", email="juan@test.com", cedula="111", telefono="123"
        )
        test_db.execute(stmt1)
        test_db.commit()
        
        with pytest.raises(Exception):
            stmt2 = insert(cliente_table).values(
                id=cliente_id_2, nombre="Carlos", email="carlos@test.com", cedula="111", telefono="456"
            )
            test_db.execute(stmt2)
            test_db.commit()

    def test_update_cliente(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id = str(uuid.uuid4())
        stmt_insert = insert(cliente_table).values(
            id=cliente_id, nombre="Juan", email="juan@test.com", cedula="111", telefono="123"
        )
        test_db.execute(stmt_insert)
        test_db.commit()
        
        stmt_update = update(cliente_table).where(
            cliente_table.c.id == cliente_id
        ).values(nombre="Carlos")
        test_db.execute(stmt_update)
        test_db.commit()
        
        query = select(cliente_table).where(cliente_table.c.id == cliente_id)
        row = test_db.execute(query).fetchone()
        assert row.nombre == "Carlos"

    def test_delete_cliente(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id = str(uuid.uuid4())
        stmt_insert = insert(cliente_table).values(
            id=cliente_id, nombre="Juan", email="juan@test.com", cedula="111", telefono="123"
        )
        test_db.execute(stmt_insert)
        test_db.commit()
        
        stmt_delete = delete(cliente_table).where(cliente_table.c.id == cliente_id)
        test_db.execute(stmt_delete)
        test_db.commit()
        
        query = select(cliente_table).where(cliente_table.c.id == cliente_id)
        result = test_db.execute(query).fetchone()
        assert result is None


class TestDatabaseTransactions:
    def test_commit_functionality(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id = str(uuid.uuid4())
        stmt = insert(cliente_table).values(
            id=cliente_id, nombre="Juan", email="juan@test.com", cedula="111", telefono="123",
            placa="ABC123", precio_por_dia=50.0, estado="disponible"
        )
        test_db.execute(stmt)
        test_db.commit()
        
        query = select(vehiculo_table).where(vehiculo_table.c.id == vehiculo_id)
        row = test_db.execute(query).fetchone()
        assert row is not None
        assert row.placa == "ABC123"

    def test_vehiculo_unique_placa(self, test_db):
        vehiculo_table = test_db.tables["vehiculo"]
        vehiculo_id_1 = str(uuid.uuid4())
        vehiculo_id_2 = str(uuid.uuid4())
        
        stmt1 = insert(vehiculo_table).values(
            id=vehiculo_id_1, tipo="auto", marca="Toyota", modelo="Corolla",
            placa="ABC123", precio_por_dia=50.0, estado="disponible"
        )
        test_db.execute(stmt1)
        test_db.commit()
        
        with pytest.raises(Exception):
            stmt2 = insert(vehiculo_table).values(
                id=vehiculo_id_2, tipo="moto", marca="Honda", modelo="CB500",
                placa="ABC123", precio_por_dia=30.0, estado="disponible"
            )
            test_db.execute(stmt2)
            test_db.commit()

    def test_update_vehiculo_precio(self, test_db):
        vehiculo_table = test_db.tables["vehiculo"]
        vehiculo_id = str(uuid.uuid4())
        stmt_insert = insert(vehiculo_table).values(
            id=vehiculo_id, tipo="auto", marca="Toyota", modelo="Corolla",
            placa="ABC123", precio_por_dia=50.0, estado="disponible"
        )
        test_db.execute(stmt_insert)
        test_db.commit()
        
        stmt_update = update(vehiculo_table).where(
            vehiculo_table.c.id == vehiculo_id
        ).values(precio_por_dia=75.0)
        test_db.execute(stmt_update)
        test_db.commit()
        
        query = select(vehiculo_table).where(vehiculo_table.c.id == vehiculo_id)
        row = test_db.execute(query).fetchone()
        assert row.precio_por_dia == 75.0

    def test_update_vehiculo_estado(self, test_db):
        vehiculo_table = test_db.tables["vehiculo"]
        vehiculo_id = str(uuid.uuid4())
        stmt_insert = insert(vehiculo_table).values(
            id=vehiculo_id, tipo="auto", marca="Toyota", modelo="Corolla",
            placa="ABC123", precio_por_dia=50.0, estado="disponible"
        )
        test_db.execute(stmt_insert)
        test_db.commit()
        
        stmt_update = update(vehiculo_table).where(
            vehiculo_table.c.id == vehiculo_id
        ).values(estado="alquilado")
        test_db.execute(stmt_update)
        test_db.commit()
        
        query = select(vehiculo_table).where(vehiculo_table.c.id == vehiculo_id)
        row = test_db.execute(query).fetchone()
        assert row.estado == "alquilado"

    def test_delete_vehiculo(self, test_db):
        vehiculo_table = test_db.tables["vehiculo"]
        vehiculo_id = str(uuid.uuid4())
        stmt_insert = insert(vehiculo_table).values(
            id=vehiculo_id, tipo="auto", marca="Toyota", modelo="Corolla",
            placa="ABC123", precio_por_dia=50.0, estado="disponible"
        )
        test_db.execute(stmt_insert)
        test_db.commit()
        
        stmt_delete = delete(vehiculo_table).where(vehiculo_table.c.id == vehiculo_id)
        test_db.execute(stmt_delete)
        test_db.commit()
        
        query = select(vehiculo_table).where(vehiculo_table.c.id == vehiculo_id)
        result = test_db.execute(query).fetchone()
        assert result is None


class TestDatabaseTransactions:
    def test_commit_functionality(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id = str(uuid.uuid4())
        stmt = insert(cliente_table).values(
            id=cliente_id, nombre="Juan Pérez", email="juan@test.com", cedula="12345678", telefono="+57 300 123 4567",
            fecha_registro="2024-01-01")
        test_db.execute(stmt)
        test_db.commit()
        
        query = select(cliente_table).where(cliente_table.c.id == cliente_id)
        result = test_db.execute(query).fetchone()
        assert result is not None

    def test_rollback_functionality(self, test_db):
        cliente_table = test_db.tables["cliente"]
        cliente_id = str(uuid.uuid4())
        stmt = insert(cliente_table).values(
            id=cliente_id, nombre="Juan", email="juan@test.com", cedula="111", telefono="123"
        )
        test_db.execute(stmt)
        test_db.rollback()
        
        query = select(cliente_table).where(cliente_table.c.id == cliente_id)
        result = test_db.execute(query).fetchone()
        assert result is None
