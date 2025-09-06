import sqlite3

conn = sqlite3.connect('database.db')

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Vehiculo(" \
            "id INT NOT NULL PRIMARY KEY AUTOINCREMENT," \
            "tipo VARCHAR(40)," \
            "marca VARCHAR(100)," \
            "modelo VARCHAR(100)," \
            "año INT," \
            "placa VARCHAR(20) UNIQUE," \
            "precio_por_dia FLOAT," \
            "caracteristicas VARCHAR(255)"    
            )

conn.commit()

cur.execute("CREATE TABLE IF NOT EXISTS Cliente(" \
            "id INT NOT NULL PRIMARY KEY AUTOINCREMENT," \
            "nombre VARCHAR(100)," \
            "email VARCHAR(100)," \
            "telefono VARCHAR(50)," \
            "dirección VARCHAR(150)," \
            "cedula VARCHAR(60))" \
            )


table3 = """
alquileres_db: List[Alquiler] = [
    Alquiler(
        id=1,
        cliente_id=2,
        vehiculo_id=4,
        fecha_inicio="2024-08-25",
        fecha_fin="2024-08-30",
        dias_alquiler=5,
        precio_total=100.0,
        estado=EstadoAlquiler.ACTIVO,
        observaciones="Cliente experimentado en motos"
    )
]
"""
