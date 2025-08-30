from typing import List, Optional, Dict, Any
from models import VehiculoCreate, VehiculoResponse
from database import execute_query, fetch_one, fetch_all

class VehiculoNotFoundError(Exception):
    """Excepción personalizada cuando no se encuentra un vehículo"""
    pass

class VehiculoDuplicateError(Exception):
    """Excepción personalizada cuando se intenta crear un vehículo duplicado"""
    pass

class VehiculoService:
    """Servicio para manejar operaciones CRUD de vehículos"""
    
    @staticmethod
    def create_vehiculo(vehiculo_data: VehiculoCreate) -> VehiculoResponse:
        """
        Crear un nuevo vehículo
        
        Args:
            vehiculo_data: Datos del vehículo a crear
            
        Returns:
            VehiculoResponse: Vehículo creado con su ID
            
        Raises:
            VehiculoDuplicateError: Si ya existe un vehículo con la misma marca, modelo y año
            Exception: Para otros errores de base de datos
        """
        try:
            # Verificar si ya existe un vehículo similar
            existing = fetch_one(
                "SELECT id FROM vehiculos WHERE marca = ? AND modelo = ? AND anio = ?",
                (vehiculo_data.marca, vehiculo_data.modelo, vehiculo_data.anio)
            )
            
            if existing:
                raise VehiculoDuplicateError(
                    f"Ya existe un vehículo {vehiculo_data.marca} {vehiculo_data.modelo} del año {vehiculo_data.anio}"
                )
            
            # Insertar el nuevo vehículo
            query = """
                INSERT INTO vehiculos 
                (marca, modelo, anio, color, precio_por_dia, disponible, tipo_vehiculo, 
                 tipo_auto, tipo_moto, cilindraje, tipo_bicicleta, tiene_cambios, numero_velocidades)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                vehiculo_data.marca,
                vehiculo_data.modelo,
                vehiculo_data.anio,
                vehiculo_data.color,
                vehiculo_data.precio_por_dia,
                vehiculo_data.disponible,
                vehiculo_data.tipo_vehiculo,
                getattr(vehiculo_data, 'tipo_auto', None),
                getattr(vehiculo_data, 'tipo_moto', None),
                getattr(vehiculo_data, 'cilindraje', None),
                getattr(vehiculo_data, 'tipo_bicicleta', None),
                getattr(vehiculo_data, 'tiene_cambios', None),
                getattr(vehiculo_data, 'numero_velocidades', None)
            )
            
            vehiculo_id = execute_query(query, params)
            
            # Obtener el vehículo creado
            return VehiculoService.get_vehiculo_by_id(vehiculo_id)
            
        except VehiculoDuplicateError:
            raise
        except Exception as e:
            raise Exception(f"Error al crear el vehículo: {str(e)}")
    
    @staticmethod
    def get_vehiculo_by_id(vehiculo_id: int) -> VehiculoResponse:
        """
        Obtener un vehículo por su ID
        
        Args:
            vehiculo_id: ID del vehículo
            
        Returns:
            VehiculoResponse: Datos del vehículo
            
        Raises:
            VehiculoNotFoundError: Si el vehículo no existe
        """
        try:
            result = fetch_one(
                "SELECT * FROM vehiculos WHERE id = ?",
                (vehiculo_id,)
            )
            
            if not result:
                raise VehiculoNotFoundError(f"Vehículo con ID {vehiculo_id} no encontrado")
            
            return VehiculoResponse(**dict(result))
            
        except VehiculoNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error al obtener el vehículo: {str(e)}")
    
    @staticmethod
    def get_all_vehiculos(
        disponible: Optional[bool] = None,
        tipo_vehiculo: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[VehiculoResponse]:
        """
        Obtener todos los vehículos con filtros opcionales
        
        Args:
            disponible: Filtrar por disponibilidad
            tipo_vehiculo: Filtrar por tipo de vehículo
            limit: Límite de resultados
            offset: Desplazamiento para paginación
            
        Returns:
            List[VehiculoResponse]: Lista de vehículos
        """
        try:
            query = "SELECT * FROM vehiculos WHERE 1=1"
            params = []
            
            # Aplicar filtros
            if disponible is not None:
                query += " AND disponible = ?"
                params.append(disponible)
            
            if tipo_vehiculo:
                query += " AND tipo_vehiculo = ?"
                params.append(tipo_vehiculo)
            
            # Ordenar por ID
            query += " ORDER BY id DESC"
            
            # Aplicar paginación
            if limit:
                query += " LIMIT ?"
                params.append(limit)
                
                if offset:
                    query += " OFFSET ?"
                    params.append(offset)
            
            results = fetch_all(query, tuple(params) if params else None)
            
            return [VehiculoResponse(**dict(row)) for row in results]
            
        except Exception as e:
            raise Exception(f"Error al obtener los vehículos: {str(e)}")
    
    @staticmethod
    def update_vehiculo_disponibilidad(vehiculo_id: int, disponible: bool) -> VehiculoResponse:
        """
        Actualizar la disponibilidad de un vehículo
        
        Args:
            vehiculo_id: ID del vehículo
            disponible: Nueva disponibilidad
            
        Returns:
            VehiculoResponse: Vehículo actualizado
            
        Raises:
            VehiculoNotFoundError: Si el vehículo no existe
        """
        try:
            # Verificar que el vehículo existe
            VehiculoService.get_vehiculo_by_id(vehiculo_id)
            
            # Actualizar disponibilidad
            execute_query(
                "UPDATE vehiculos SET disponible = ? WHERE id = ?",
                (disponible, vehiculo_id)
            )
            
            # Retornar el vehículo actualizado
            return VehiculoService.get_vehiculo_by_id(vehiculo_id)
            
        except VehiculoNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error al actualizar la disponibilidad: {str(e)}")
    
    @staticmethod
    def delete_vehiculo(vehiculo_id: int) -> bool:
        """
        Eliminar un vehículo (soft delete - marcar como no disponible)
        
        Args:
            vehiculo_id: ID del vehículo
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            VehiculoNotFoundError: Si el vehículo no existe
        """
        try:
            # Verificar que el vehículo existe
            VehiculoService.get_vehiculo_by_id(vehiculo_id)
            
            # Marcar como no disponible en lugar de eliminar físicamente
            execute_query(
                "UPDATE vehiculos SET disponible = 0 WHERE id = ?",
                (vehiculo_id,)
            )
            
            return True
            
        except VehiculoNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error al eliminar el vehículo: {str(e)}")
    
    @staticmethod
    def get_vehiculos_stats() -> Dict[str, Any]:
        """
        Obtener estadísticas básicas de los vehículos
        
        Returns:
            Dict con estadísticas básicas
        """
        try:
            total = fetch_one("SELECT COUNT(*) as count FROM vehiculos")[0]
            disponibles = fetch_one("SELECT COUNT(*) as count FROM vehiculos WHERE disponible = 1")[0]
            no_disponibles = total - disponibles
            
            tipos = fetch_all("""
                SELECT tipo_vehiculo, COUNT(*) as count 
                FROM vehiculos 
                GROUP BY tipo_vehiculo
            """)
            
            tipos_dict = {row[0]: row[1] for row in tipos}
            
            return {
                "total_vehiculos": total,
                "vehiculos_disponibles": disponibles,
                "vehiculos_no_disponibles": no_disponibles,
                "por_tipo": tipos_dict
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener estadísticas: {str(e)}")
