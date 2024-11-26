from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

class CRUDUser:
    def get_by_username(self, db: Session, username: str) -> User:
        """Obtiene un usuario por su nombre de usuario."""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> User:
        """Obtiene un usuario por su correo electrónico."""
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """Crea un nuevo usuario en la base de datos."""
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, username: str, password: str) -> User:
        """Autentica un usuario verificando su nombre de usuario y contraseña."""
        user = self.get_by_username(db, username=username)
        if not user:
            print("Error: Usuario no encontrado")  # Mensaje para depuración
            return None
        if not verify_password(password, user.hashed_password):
            print("Error: Contraseña incorrecta")  # Mensaje para depuración
            return None
        return user

crud_user = CRUDUser()
