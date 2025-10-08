from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

class Site(Base):
    __tablename__ = "site"
    
    id = mapped_column(Integer, primary_key=True)  # <-- columna primaria correcta
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(255))
