from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.core.board.site import Site
from src.core.board.tag import Tag

class SiteTag(Base):
    __tablename__ = "site_tag"
    site_id = Column(Integer, ForeignKey("site.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    site = relationship("Site", back_populates="tags")
    tag = relationship("Tag", back_populates="sites")