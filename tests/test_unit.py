import pytest
from datetime import datetime, timedelta
from models.cliente import ClienteCreate, ClienteUpdate
from models.Vehiculo import VehiculoCreate, VehiculoUpdate, TipoVehiculo
from models.alquiler import AlquilerCreate, CalcularCosto


class TestClienteModels:
    def test_cliente_create_valid(self):
        cliente = ClienteCreate(
            nombre="Juan Pérez",
            email="juan@example.com",
            telefono="+57 300 123 4567",
            cedula="12345678",
            direccion="Calle 1"
        )
        assert cliente.nombre == "Juan Pérez"
        assert cliente.email == "juan@example.com"
        assert cliente.cedula == "12345678"

    def test_cliente_create_required_fields(self):
        with pytest.raises(Exception):
            ClienteCreate(
                nombre="Juan",
                email="juan@example.com"
            )

    def test_cliente_update_partial(self):
        update = ClienteUpdate(nombre="Carlos")
        assert update.nombre == "Carlos"
        assert update.email is None

    def test_cliente_update_empty(self):
        update = ClienteUpdate()
        assert update.model_dump(exclude_unset=True) == {}


class TestVehiculoModels:
    def test_vehiculo_create_valid(self):
        vehiculo = VehiculoCreate(
            tipo=TipoVehiculo.AUTO,
            marca="Toyota",
            modelo="Corolla",
            placa="ABC123",
            precio_por_dia=50.0
        )
        assert vehiculo.tipo == TipoVehiculo.AUTO
        assert vehiculo.marca == "Toyota"
        assert vehiculo.precio_por_dia == 50.0

    def test_vehiculo_create_invalid_tipo(self):
        with pytest.raises(Exception):
            VehiculoCreate(
                tipo="invalido",
                marca="Toyota",
                modelo="Corolla",
                placa="ABC123",
                precio_por_dia=50.0
            )

    def test_vehiculo_update_price(self):
        update = VehiculoUpdate(precio_por_dia=75.0)
        assert update.precio_por_dia == 75.0
        assert update.marca is None


class TestAlquilerModels:
    def test_alquiler_create_valid(self):
        hoy = datetime.now()
        fin = hoy + timedelta(days=5)
        
        alquiler = AlquilerCreate(
            cliente_id="123",
            vehiculo_id="456",
            fecha_inicio=hoy.strftime("%Y-%m-%d"),
            fecha_fin=fin.strftime("%Y-%m-%d")
        )
        assert alquiler.cliente_id == "123"
        assert alquiler.vehiculo_id == "456"

    def test_alquiler_create_missing_fields(self):
        with pytest.raises(Exception):
            AlquilerCreate(
                cliente_id="123",
                vehiculo_id="456"
            )

    def test_calculo_costo_valid(self):
        hoy = datetime.now()
        fin = hoy + timedelta(days=5)
        
        costo = CalcularCosto(
            vehiculo_id="123",
            fecha_inicio=hoy.strftime("%Y-%m-%d"),
            fecha_fin=fin.strftime("%Y-%m-%d")
        )
        assert costo.vehiculo_id == "123"


class TestEnumValues:
    def test_tipo_vehiculo_values(self):
        assert TipoVehiculo.AUTO.value == "auto"
        assert TipoVehiculo.MOTO.value == "moto"
        assert TipoVehiculo.BICICLETA.value == "bicicleta"

    def test_cliente_email_format(self):
        cliente = ClienteCreate(
            nombre="Test",
            email="test@example.com",
            telefono="123456",
            cedula="123"
        )
        assert "@" in cliente.email


class TestFieldValidations:
    def test_cliente_cedula_string(self):
        cliente = ClienteCreate(
            nombre="Test",
            email="test@example.com",
            telefono="123",
            cedula="123456789"
        )
        assert isinstance(cliente.cedula, str)

    def test_vehiculo_price_positive(self):
        vehiculo = VehiculoCreate(
            tipo=TipoVehiculo.AUTO,
            marca="Toyota",
            modelo="Corolla",
            placa="ABC123",
            precio_por_dia=0.01
        )
        assert vehiculo.precio_por_dia > 0

    def test_vehiculo_precio_negative_allowed(self):
        vehiculo = VehiculoCreate(
            tipo=TipoVehiculo.AUTO,
            marca="Toyota",
            modelo="Corolla",
            placa="ABC123",
            precio_por_dia=-50.0
        )
        assert vehiculo.precio_por_dia == -50.0
