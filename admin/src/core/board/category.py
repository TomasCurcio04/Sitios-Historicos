from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    sites = relationship("Site", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
