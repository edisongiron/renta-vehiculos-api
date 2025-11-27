# Testing

Proyecto con suite completa de tests: unit, integration, API y database.

## Instalación

```bash
pipenv shell -> Para iniciar el entorno virtual
pipenv install -> Instalar TODAS las dependencias
```

## Ejecución

Todos los tests:
```bash
pytest
```

Tests específicos:

```bash
pytest tests/test_unit.py
pytest tests/test_db.py
pytest tests/test_api.py
pytest tests/test_integration.py
```

Con más detalle:
```bash
pytest -v
```

Mostrar solo fallos:
```bash
pytest --tb=short
```

## Estructura de Tests

**test_unit.py**: Pruebas unitarias de modelos Pydantic sin dependencias de BD. Valida esquemas, enums y validaciones de campos.

**test_db.py**: Pruebas de SQLAlchemy con BD en memoria. Valida CRUD, constraints únicos, transacciones y rollback.

**test_api.py**: Pruebas de endpoints HTTP con TestClient. Valida status codes, formatos de respuesta y errores.

**test_integration.py**: Pruebas de flujos completos entre capas. Valida controllers, endpoints y casos de uso reales.

## Cobertura

```bash
pytest --cov=controllers --cov=models --cov-report=html
```
