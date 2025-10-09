


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.core.database import Base

# -------------------------------
# Tabla Tag
# -------------------------------
class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = {"extend_existing": True}

    id_tag = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<Tag(id_tag={self.id_tag}, name='{self.name}')>"

# -------------------------------
# Tabla Category
# -------------------------------
class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"extend_existing": True}

    id_category = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<Category(id_category={self.id_category}, name='{self.name}')>"

# -------------------------------
# Tabla State
# -------------------------------
class State(Base):
    __tablename__ = "state"
    __table_args__ = {"extend_existing": True}

    id_state = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<State(id_state={self.id_state}, name='{self.name}')>"

# -------------------------------
# Tabla SiteHistory
# -------------------------------
class SiteHistory(Base):
    __tablename__ = "site_history"
    __table_args__ = {"extend_existing": True}

    id_site_history = Column(Integer, primary_key=True)
    description = Column(String)

# -------------------------------
# Tabla Users
# -------------------------------
class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id_user = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)

# -------------------------------
# Tabla Role
# -------------------------------
class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}

    id_role = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# -------------------------------
# Tabla Permission
# -------------------------------
class Permission(Base):
    __tablename__ = "permission"
    __table_args__ = {"extend_existing": True}

    id_permission = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# -------------------------------
# Tabla PermissionList
# -------------------------------
class PermissionList(Base):
    __tablename__ = "permission_list"
    __table_args__ = {"extend_existing": True}

    id_permission_list = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id_role"))
    permission_id = Column(Integer, ForeignKey("permission.id_permission"))

# -------------------------------
# Tabla FeatureFlag
# -------------------------------
class FeatureFlag(Base):
    __tablename__ = "feature_flag"
    __table_args__ = {"extend_existing": True}

    id_flag = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    enabled = Column(Boolean, default=False)