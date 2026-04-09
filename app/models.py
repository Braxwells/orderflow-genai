import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class CanalEnum(str, enum.Enum):
    whatsapp = "whatsapp"
    email = "email"


class EstadoEnum(str, enum.Enum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    enviado = "enviado"


class RolEnum(str, enum.Enum):
    admin = "admin"
    empleado = "empleado"


class Usuario(Base):
    __tablename__ = "usuarios"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), unique=True, nullable=False, index=True)
    nombre        = Column(String(100), nullable=False)
    password_hash = Column(String, nullable=False)
    rol           = Column(Enum(RolEnum), default=RolEnum.empleado, nullable=False)
    activo        = Column(Boolean, default=True, nullable=False)

    pedidos = relationship("Pedido", back_populates="creador")


class Pedido(Base):
    __tablename__ = "pedidos"

    id             = Column(Integer, primary_key=True, index=True)
    cliente        = Column(String(100), nullable=False)
    articulo       = Column(String(200), nullable=False)
    talla          = Column(String(20), nullable=False)
    precio         = Column(Float, nullable=False)
    canal          = Column(Enum(CanalEnum), nullable=False)
    estado         = Column(Enum(EstadoEnum), default=EstadoEnum.pendiente, nullable=False)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    fecha_envio    = Column(DateTime, nullable=True)
    creado_por     = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    creador = relationship("Usuario", back_populates="pedidos")