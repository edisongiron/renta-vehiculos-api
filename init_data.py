"""
Script para inicializar datos básicos en la base de datos
- Estados de alquiler
- Roles de usuario
- Usuario administrador inicial
"""

from sqlalchemy import insert, select
from database.db import engine, meta
from schemas.estado_alquiler import estado_alquiler
from schemas.roles import roles  
from schemas.auth_usuarios import auth_usuarios
from utils.auth_utils import get_password_hash
import uuid
from datetime import datetime

def init_database():
    """Inicializa la base de datos creando las tablas"""
    print("Creando tablas...")
    meta.create_all(engine)
    print("Tablas creadas exitosamente!")

def init_estados_alquiler():
    """Inicializa los estados de alquiler"""
    print("Inicializando estados de alquiler...")
    
    with engine.begin() as conn:
        # Verificar si ya existen estados
        query = select(estado_alquiler)
        existing_states = conn.execute(query).fetchall()
        
        if not existing_states:
            estados = [
                {"id": 1, "nombre": "activo"},
                {"id": 2, "nombre": "completado"}, 
                {"id": 3, "nombre": "cancelado"}
            ]
            
            for estado in estados:
                insert_query = insert(estado_alquiler).values(estado)
                conn.execute(insert_query)
            
            print("Estados de alquiler creados: activo, completado, cancelado")
        else:
            print("Estados de alquiler ya existen")

def init_roles():
    """Inicializa los roles de usuario"""
    print("Inicializando roles...")
    
    with engine.begin() as conn:
        # Verificar si ya existen roles
        query = select(roles)
        existing_roles = conn.execute(query).fetchall()
        
        if not existing_roles:
            roles_data = [
                {"id": 1, "nombre": "administrador", "descripcion": "Usuario administrador con acceso total"},
                {"id": 2, "nombre": "empleado", "descripcion": "Empleado con acceso a operaciones"},
                {"id": 3, "nombre": "usuario", "descripcion": "Usuario regular del sistema"}
            ]
            
            for role in roles_data:
                insert_query = insert(roles).values(role)
                conn.execute(insert_query)
            
            print("Roles creados: administrador, empleado, usuario")
        else:
            print("Roles ya existen")

def init_admin_user():
    """Crea el usuario administrador inicial"""
    print("Inicializando usuario administrador...")
    
    with engine.begin() as conn:
        # Verificar si ya existe un admin
        query = select(auth_usuarios).where(auth_usuarios.c.username == "admin")
        existing_admin = conn.execute(query).first()
        
        if not existing_admin:
            admin_id = str(uuid.uuid4())
            admin_data = {
                "id": admin_id,
                "username": "admin",
                "email": "admin@sistema.com",
                "password_hash": get_password_hash("admin123"),
                "nombre_completo": "Administrador del Sistema",
                "activo": True,
                "rol_id": 1,  # Administrador
                "fecha_creacion": datetime.utcnow(),
                "creado_por": admin_id  # Self-reference para el primer usuario
            }
            
            insert_query = insert(auth_usuarios).values(admin_data)
            conn.execute(insert_query)
            
            print("Usuario administrador creado:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@sistema.com")
            print("¡IMPORTANTE: Cambia la contraseña después del primer login!")
        else:
            print("Usuario administrador ya existe")

def main():
    """Función principal"""
    print("=== Inicializando base de datos ===")
    
    try:
        # Crear tablas
        init_database()
        
        # Inicializar datos básicos
        init_estados_alquiler()
        init_roles()
        init_admin_user()
        
        print("\n=== Inicialización completada exitosamente ===")
        print("\nCredenciales del administrador:")
        print("Username: admin")
        print("Password: admin123")
        print("\n¡Recuerda cambiar la contraseña después del primer login!")
        
    except Exception as e:
        print(f"Error durante la inicialización: {str(e)}")
        raise

if __name__ == "__main__":
    main()
