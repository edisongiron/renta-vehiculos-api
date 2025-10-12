from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Configurar engine con check_same_thread=False para SQLite
engine = create_engine(
    "sqlite:///database.db",
    echo=False,
    connect_args={"check_same_thread": False},  # Permite uso en múltiples threads
)

meta = MetaData()

# Crear una sesión para transacciones
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


# Función para obtener sesión de base de datos (dependency injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Para mantener compatibilidad temporal con código existente
# DEPRECATED: usar get_db() en su lugar
conn = engine.connect()
