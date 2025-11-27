import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from database.db import get_db
import uuid


@pytest.fixture
def test_db():
    from utils.auth_utils import get_current_user
    
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    from schemas.clientes import cliente as clientes_table
    from schemas.vehiculo import vehiculo as vehiculos_table
    from schemas.alquileres import alquileres as alquileres_table
    
    clientes_table.metadata.create_all(engine)
    vehiculos_table.metadata.create_all(engine)
    alquileres_table.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    
    def override_get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
    
    def override_get_current_user():
        return {"user_id": "test-user", "email": "test@example.com"}
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield SessionLocal()


@pytest.fixture
def client(test_db):
    return TestClient(app)


class TestRootEndpoint:
    def test_root_get(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Bienvenido a la API de Alquiler de Vehículos"

    def test_root_version(self, client):
        response = client.get("/")
        assert response.json()["version"] == "1.0.0"


class TestClientesEndpoints:
    def test_obtener_clientes_empty(self, client):
        response = client.get("/clientes/")
        assert response.status_code == 200
        assert response.json() == []

    def test_crear_cliente(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        response = client.post("/clientes/", json=cliente_data)
        assert response.status_code == 201
        assert response.json()["nombre"] == "Juan Pérez"
        assert response.json()["email"] == "juan@test.com"

    def test_crear_cliente_email_duplicado(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        cliente_data2 = {
            "nombre": "Carlos",
            "email": "juan@test.com",
            "telefono": "+57 300 987 6543",
            "cedula": "87654321",
            "direccion": "Calle 2"
        }
        response = client.post("/clientes/", json=cliente_data2)
        assert response.status_code == 400

    def test_crear_cliente_cedula_duplicada(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        cliente_data2 = {
            "nombre": "Carlos",
            "email": "carlos@test.com",
            "telefono": "+57 300 987 6543",
            "cedula": "12345678",
            "direccion": "Calle 2"
        }
        response = client.post("/clientes/", json=cliente_data2)
        assert response.status_code == 400

    def test_obtener_clientes_con_busqueda(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        response = client.get("/clientes/?buscar=Juan")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_obtener_cliente_por_cedula(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        response = client.get("/clientes/12345678")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Juan Pérez"

    def test_obtener_cliente_no_existe(self, client):
        response = client.get("/clientes/999999")
        assert response.status_code == 404

    def test_actualizar_cliente(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        update_data = {"nombre": "Carlos"}
        response = client.put("/clientes/12345678", json=update_data)
        assert response.status_code == 200
        assert response.json()["nombre"] == "Carlos"

    def test_actualizar_cliente_no_existe(self, client):
        update_data = {"nombre": "Carlos"}
        response = client.put("/clientes/999999", json=update_data)
        assert response.status_code == 404


class TestVehiculosEndpoints:
    def test_obtener_vehiculos_empty(self, client):
        response = client.get("/vehiculos/")
        assert response.status_code == 200
        assert response.json() == []

    def test_crear_vehiculo(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        response = client.post("/vehiculos/", json=vehiculo_data)
        assert response.status_code == 201
        assert response.json()["marca"] == "Toyota"
        assert response.json()["placa"] == "ABC123"

    def test_crear_vehiculo_placa_duplicada(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        client.post("/vehiculos/", json=vehiculo_data)
        
        vehiculo_data2 = {
            "tipo": "moto",
            "marca": "Honda",
            "modelo": "CB500",
            "placa": "ABC123",
            "precio_por_dia": 30.0
        }
        response = client.post("/vehiculos/", json=vehiculo_data2)
        assert response.status_code == 400

    def test_obtener_vehiculo_por_id(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        create_response = client.post("/vehiculos/", json=vehiculo_data)
        vehiculo_id = create_response.json()["id"]
        
        response = client.get(f"/vehiculos/{vehiculo_id}")
        assert response.status_code == 200
        assert response.json()["id"] == vehiculo_id

    def test_obtener_vehiculo_no_existe(self, client):
        response = client.get(f"/vehiculos/{str(uuid.uuid4())}")
        assert response.status_code == 404

    def test_actualizar_vehiculo(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        create_response = client.post("/vehiculos/", json=vehiculo_data)
        vehiculo_id = create_response.json()["id"]
        
        update_data = {"precio_por_dia": 75.0}
        response = client.put(f"/vehiculos/{vehiculo_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["precio_por_dia"] == 75.0

    def test_actualizar_vehiculo_no_existe(self, client):
        update_data = {"precio_por_dia": 75.0}
        response = client.put(f"/vehiculos/{str(uuid.uuid4())}", json=update_data)
        assert response.status_code == 404

    def test_verificar_disponibilidad(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        create_response = client.post("/vehiculos/", json=vehiculo_data)
        vehiculo_id = create_response.json()["id"]
        
        response = client.get(f"/vehiculos/{vehiculo_id}/disponibilidad")
        assert response.status_code == 200
        assert response.json()["disponible"] is True


class TestResponseFormats:
    def test_cliente_response_format(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        response = client.post("/clientes/", json=cliente_data)
        data = response.json()
        
        assert "id" in data
        assert "nombre" in data
        assert "email" in data
        assert "cedula" in data

    def test_vehiculo_response_format(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        response = client.post("/vehiculos/", json=vehiculo_data)
        data = response.json()
        
        assert "id" in data
        assert "tipo" in data
        assert "placa" in data


class TestStatusCodes:
    def test_post_status_codes(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        response = client.post("/clientes/", json=cliente_data)
        assert response.status_code == 201

    def test_get_status_code(self, client):
        response = client.get("/clientes/")
        assert response.status_code == 200

    def test_put_status_code(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        update_data = {"nombre": "Carlos"}
        response = client.put("/clientes/12345678", json=update_data)
        assert response.status_code == 200
