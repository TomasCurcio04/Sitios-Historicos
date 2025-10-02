from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

class User(Base):
        __tablename_ = "users"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        nombre: Mapped[str] = mapped_column(nullable=False)
        email: Mapped[str] = mapped_column(unique=True, nullable=False)
        password: Mapped[str] = mapped_column(nullable=False)
        is_active: Mapped[bool] = mapped_column(default=True)

        creation_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
        
        rol: Mapped[str] = mapped_column(nullable=False) # Hay que cambiarlo a un enum
