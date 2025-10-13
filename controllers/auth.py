from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from schemas.auth_usuarios import auth_usuarios
from schemas.roles import roles
from models.auth import (
    UserLogin,
    UserRegister,
    UserResponse,
    TokenResponse,
    PasswordChange,
)
from utils.auth_utils import (
    authenticate_user,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import uuid


class Auth:
    """
    Controlador para gestionar la autenticación y registro de usuarios.
    
    Esta clase maneja todas las operaciones relacionadas con autenticación,
    incluyendo login, registro de nuevos usuarios y gestión de tokens JWT.
    """

    @staticmethod
    def login(user_data: UserLogin, db: Session):
        """
        Autentica un usuario y genera un token de acceso JWT.
        
        Verifica las credenciales del usuario, actualiza la fecha de último login
        y genera un token JWT con tiempo de expiración configurado.
        
        Args:
            user_data: Credenciales del usuario (username y password)
            db: Sesión de base de datos SQLAlchemy
            
        Returns:
            TokenResponse con el token JWT y datos del usuario autenticado
            
        Raises:
            HTTPException: Si las credenciales son inválidas o hay error del servidor
        """
        try:
            user = authenticate_user(user_data.username, user_data.password, db)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                )

            update_query = (
                update(auth_usuarios)
                .where(auth_usuarios.c.id == user["id"])
                .values(ultimo_login=datetime.utcnow())
            )
            db.execute(update_query)
            db.commit()

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user["id"]}, expires_delta=access_token_expires
            )

            user_response = UserResponse(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                nombre_completo=user["nombre_completo"],
                activo=user["activo"],
                rol_id=user["rol_id"],
                fecha_creacion=None,
                ultimo_login=datetime.utcnow(),
            )

            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user=user_response,
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}",
            )

    @staticmethod
    def register(user_data: UserRegister, db: Session):
        """
        Registra un nuevo usuario en el sistema.
        
        Valida que el username y email no estén duplicados, verifica la existencia
        del rol y crea el usuario con contraseña hasheada.
        
        Args:
            user_data: Datos del nuevo usuario a registrar
            db: Sesión de base de datos SQLAlchemy
            
        Returns:
            UserResponse con los datos del usuario creado
            
        Raises:
            HTTPException: Si username/email duplicados, rol inválido o error al crear
        """
        try:
            query = select(auth_usuarios).where(
                auth_usuarios.c.username == user_data.username
            )
            existing_user = db.execute(query).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está registrado",
                )

            query = select(auth_usuarios).where(
                auth_usuarios.c.email == user_data.email
            )
            existing_email = db.execute(query).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado",
                )

            if user_data.rol_id:
                role_query = select(roles).where(roles.c.id == user_data.rol_id)
                role_exists = db.execute(role_query).first()
                if not role_exists:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El rol especificado no existe",
                    )

            hashed_password = get_password_hash(user_data.password)

            user_id = str(uuid.uuid4())
            insert_query = insert(auth_usuarios).values(
                id=user_id,
                username=user_data.username,
                email=user_data.email,
                password_hash=hashed_password,
                nombre_completo=user_data.nombre_completo,
                activo=True,
                rol_id=user_data.rol_id or 2,
                fecha_creacion=datetime.utcnow(),
            )

            db.execute(insert_query)
            db.commit()

            user_query = select(auth_usuarios).where(auth_usuarios.c.id == user_id)
            created_user = db.execute(user_query).first()

            return UserResponse(
                id=created_user.id,
                username=created_user.username,
                email=created_user.email,
                nombre_completo=created_user.nombre_completo,
                activo=created_user.activo,
                rol_id=created_user.rol_id,
                fecha_creacion=created_user.fecha_creacion,
                ultimo_login=created_user.ultimo_login,
            )

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar usuario: {str(e)}",
            )
