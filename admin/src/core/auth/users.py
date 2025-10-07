# pylint: disable=import-error
"""Modelo de usuario para la tabla 'users' en la base de datos."""
import bcrypt
import re
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.board.site import Site

#Expresion regular para validar emails
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

class Users(Base):
    """Modelo de usuario para la tabla 'users'."""

    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[int] = mapped_column(ForeignKey("role.id_role"), nullable=False)
    rol_rel: Mapped["Role"] = relationship(back_populates="users")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    s_user: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sites: Mapped[list["Site"]] = relationship(back_populates="user")
    user_history: Mapped[list["SiteHistory"]] = relationship(back_populates="user_rel")
    date_create: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    modify: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @validates("email")
    def validate_email(self, key, email):
        """Asegura que el email tiene un formato válido."""
        
        email = email.strip()
        
        if not re.match(EMAIL_REGEX, email):
            raise ValueError("Formato de email inválido")
        
        return email

    def verificar_password(self, password: str) -> bool:        
        """Verifica una contraseña de texto plano contra el hash almacenado."""
        # Codificar la contraseña ingresada y el hash almacenado a bytes
        stored_hash = self.pass_.encode('utf-8')
        input_password = password.encode('utf-8')
        
        # Usar checkpw para una verificación segura contra ataques de tiempo
        return bcrypt.checkpw(input_password, stored_hash)

    
    def __repr__(self):
        return f"<Users(user_name='{self.user_name}', email='{self.email}', role={self.role})>"

