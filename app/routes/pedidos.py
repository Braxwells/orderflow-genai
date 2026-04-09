from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Pedido, EstadoEnum, CanalEnum, Usuario
from app.security import get_current_user
from datetime import datetime, timezone

router = APIRouter()


class PedidoCreate(BaseModel):
    cliente: str
    articulo: str
    talla: str
    precio: float
    canal: CanalEnum


class PedidoUpdate(BaseModel):
    cliente: Optional[str] = None
    articulo: Optional[str] = None
    talla: Optional[str] = None
    precio: Optional[float] = None
    canal: Optional[CanalEnum] = None


class EstadoUpdate(BaseModel):
    estado: EstadoEnum


@router.get("/")
def listar_pedidos(
    estado: Optional[EstadoEnum] = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    query = db.query(Pedido).filter(Pedido.estado != EstadoEnum.enviado)
    if estado:
        query = query.filter(Pedido.estado == estado)
    return query.order_by(Pedido.fecha_creacion.asc()).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    pedido = Pedido(
        cliente=data.cliente,
        articulo=data.articulo,
        talla=data.talla,
        precio=data.precio,
        canal=data.canal,
        creado_por=current_user.id
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


@router.put("/{pedido_id}")
def editar_pedido(
    pedido_id: int,
    data: PedidoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.estado == EstadoEnum.enviado:
        raise HTTPException(status_code=403, detail="No se puede editar un pedido del histórico")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pedido, field, value)

    db.commit()
    db.refresh(pedido)
    return pedido


@router.patch("/{pedido_id}/estado")
def cambiar_estado(
    pedido_id: int,
    data: EstadoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.estado == EstadoEnum.enviado:
        raise HTTPException(status_code=403, detail="El pedido ya está en el histórico")

    pedido.estado = data.estado
    if data.estado == EstadoEnum.enviado:
        pedido.fecha_envio = datetime.now(timezone.utc)

    db.commit()
    db.refresh(pedido)
    return pedido