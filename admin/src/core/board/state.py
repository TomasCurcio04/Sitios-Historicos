from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base

class State(Base):
    __tablename__ = "state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    sites = relationship("Site", back_populates="state")

    def __repr__(self):
        return f"<State(id={self.id}, name='{self.name}')>"
