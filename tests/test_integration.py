import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from database.db import get_db
from controllers.clientes import Clientes
from controllers.vehiculos import Vehiculos
from models.cliente import ClienteCreate, ClienteUpdate
from models.Vehiculo import VehiculoCreate, VehiculoUpdate, TipoVehiculo
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


class TestClienteIntegration:
    def test_crear_obtener_actualizar_cliente_flujo_completo(self, test_db, client):
        cliente_create = ClienteCreate(
            nombre="Juan Pérez",
            email="juan@test.com",
            telefono="+57 300 123 4567",
            cedula="12345678",
            direccion="Calle 1"
        )
        
        cliente = Clientes.crear_cliente(test_db, cliente_create)
        assert cliente.nombre == "Juan Pérez"
        
        cliente_recuperado = Clientes.obtener_cliente(test_db, "12345678")
        assert cliente_recuperado.email == "juan@test.com"
        
        update = ClienteUpdate(nombre="Carlos")
        cliente_actualizado = Clientes.actualizar_cliente(test_db, "12345678", update)
        assert cliente_actualizado.nombre == "Carlos"

    def test_crear_cliente_controller_endpoint_integracion(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        response = client.post("/clientes/", json=cliente_data)
        assert response.status_code == 201
        cliente_id = response.json()["id"]
        
        get_response = client.get(f"/clientes/12345678")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == cliente_id

    def test_listar_clientes_con_filtro(self, test_db, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        client.post("/clientes/", json=cliente_data)
        
        cliente_data2 = {
            "nombre": "Carlos López",
            "email": "carlos@test.com",
            "telefono": "+57 300 987 6543",
            "cedula": "87654321",
            "direccion": "Calle 2"
        }
        client.post("/clientes/", json=cliente_data2)
        
        response = client.get("/clientes/?buscar=Juan")
        assert len(response.json()) == 1


class TestVehiculoIntegration:
    def test_crear_obtener_actualizar_vehiculo_flujo_completo(self, test_db, client):
        vehiculo_create = VehiculoCreate(
            tipo=TipoVehiculo.AUTO,
            marca="Toyota",
            modelo="Corolla",
            placa="ABC123",
            precio_por_dia=50.0
        )
        
        vehiculo = Vehiculos.crear_vehiculo(test_db, vehiculo_create)
        assert vehiculo.marca == "Toyota"
        vehiculo_id = vehiculo.id
        
        vehiculo_recuperado = Vehiculos.obtener_vehiculo(test_db, vehiculo_id)
        assert vehiculo_recuperado.placa == "ABC123"
        
        update = VehiculoUpdate(precio_por_dia=75.0)
        vehiculo_actualizado = Vehiculos.actualizar_vehiculo(test_db, vehiculo_id, update)
        assert vehiculo_actualizado.precio_por_dia == 75.0

    def test_crear_vehiculo_controller_endpoint_integracion(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        response = client.post("/vehiculos/", json=vehiculo_data)
        assert response.status_code == 201
        vehiculo_id = response.json()["id"]
        
        get_response = client.get(f"/vehiculos/{vehiculo_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == vehiculo_id

    def test_disponibilidad_vehiculo_flujo(self, test_db, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        create_response = client.post("/vehiculos/", json=vehiculo_data)
        vehiculo_id = create_response.json()["id"]
        
        disponibilidad = Vehiculos.verificar_disponibilidad(test_db, vehiculo_id)
        assert disponibilidad.disponible is True
        assert disponibilidad.vehiculo_id == vehiculo_id


class TestClienteVehiculoIntegracion:
    def test_crear_cliente_y_vehiculo_multiples(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        cliente_response = client.post("/clientes/", json=cliente_data)
        assert cliente_response.status_code == 201
        
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        vehiculo_response = client.post("/vehiculos/", json=vehiculo_data)
        assert vehiculo_response.status_code == 201
        
        vehiculo_data2 = {
            "tipo": "moto",
            "marca": "Honda",
            "modelo": "CB500",
            "placa": "DEF456",
            "precio_por_dia": 30.0
        }
        vehiculo_response2 = client.post("/vehiculos/", json=vehiculo_data2)
        assert vehiculo_response2.status_code == 201


class TestDataValidation:
    def test_cliente_validacion_email_unico_multiples_intentos(self, client):
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "telefono": "+57 300 123 4567",
            "cedula": "12345678",
            "direccion": "Calle 1"
        }
        response1 = client.post("/clientes/", json=cliente_data)
        assert response1.status_code == 201
        
        cliente_data["cedula"] = "87654321"
        response2 = client.post("/clientes/", json=cliente_data)
        assert response2.status_code == 400
        assert "email" in response2.json()["detail"].lower() or "ya está" in response2.json()["detail"].lower()

    def test_vehiculo_validacion_placa_unica_multiples_intentos(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        response1 = client.post("/vehiculos/", json=vehiculo_data)
        assert response1.status_code == 201
        
        vehiculo_data["tipo"] = "moto"
        response2 = client.post("/vehiculos/", json=vehiculo_data)
        assert response2.status_code == 400

    def test_actualizacion_cliente_con_datos_parciales(self, client):
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
        assert response.json()["email"] == "juan@test.com"

    def test_actualizacion_vehiculo_solo_precio(self, client):
        vehiculo_data = {
            "tipo": "auto",
            "marca": "Toyota",
            "modelo": "Corolla",
            "placa": "ABC123",
            "precio_por_dia": 50.0
        }
        create_response = client.post("/vehiculos/", json=vehiculo_data)
        vehiculo_id = create_response.json()["id"]
        
        update_data = {"precio_por_dia": 100.0}
        response = client.put(f"/vehiculos/{vehiculo_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["precio_por_dia"] == 100.0
        assert response.json()["marca"] == "Toyota"


class TestErrorHandling:
    def test_obtener_cliente_no_existente(self, test_db):
        with pytest.raises(Exception):
            Clientes.obtener_cliente(test_db, "999999")

    def test_actualizar_cliente_no_existente(self, test_db):
        update = ClienteUpdate(nombre="Test")
        with pytest.raises(Exception):
            Clientes.actualizar_cliente(test_db, "999999", update)

    def test_obtener_vehiculo_no_existente(self, test_db):
        with pytest.raises(Exception):
            Vehiculos.obtener_vehiculo(test_db, str(uuid.uuid4()))

    def test_actualizar_vehiculo_no_existente(self, test_db):
        update = VehiculoUpdate(precio_por_dia=100.0)
        with pytest.raises(Exception):
            Vehiculos.actualizar_vehiculo(test_db, str(uuid.uuid4()), update)


class TestCRUDOperations:
    def test_crear_multiple_clientes(self, client):
        for i in range(5):
            cliente_data = {
                "nombre": f"Cliente {i}",
                "email": f"cliente{i}@test.com",
                "telefono": f"+57 300 000 {i:04d}",
                "cedula": f"{i:08d}",
                "direccion": f"Calle {i}"
            }
            response = client.post("/clientes/", json=cliente_data)
            assert response.status_code == 201
        
        list_response = client.get("/clientes/")
        assert len(list_response.json()) == 5

    def test_crear_multiple_vehiculos(self, client):
        tipos = ["auto", "moto", "bicicleta"]
        for i in range(5):
            vehiculo_data = {
                "tipo": tipos[i % 3],
                "marca": f"Marca {i}",
                "modelo": f"Modelo {i}",
                "placa": f"PLK{i:04d}",
                "precio_por_dia": 50.0 + (i * 10)
            }
            response = client.post("/vehiculos/", json=vehiculo_data)
            assert response.status_code == 201
        
        list_response = client.get("/vehiculos/")
        assert len(list_response.json()) == 5
