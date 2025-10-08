from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.core.database import Base

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), nullable=False, unique=True)
    date_created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    sites = relationship("SiteTag", back_populates="tag")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"
