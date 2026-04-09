import csv
import io
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pedido, EstadoEnum, Usuario
from app.security import get_current_user, require_admin

router = APIRouter()


@router.get("/")
def listar_historico(
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    query = db.query(Pedido).filter(Pedido.estado == EstadoEnum.enviado)
    if q:
        query = query.filter(
            Pedido.cliente.ilike(f"%{q}%") |
            Pedido.articulo.ilike(f"%{q}%")
        )
    return query.order_by(Pedido.fecha_envio.desc()).all()


@router.get("/export")
def exportar_csv(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    pedidos = db.query(Pedido).filter(
        Pedido.estado == EstadoEnum.enviado
    ).order_by(Pedido.fecha_envio.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Cliente", "Artículo", "Talla", "Precio",
                     "Canal", "Fecha creación", "Fecha envío"])
    for p in pedidos:
        writer.writerow([
            p.id, p.cliente, p.articulo, p.talla, p.precio,
            p.canal.value,
            p.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            p.fecha_envio.strftime("%Y-%m-%d %H:%M") if p.fecha_envio else ""
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=historico_orderflow.csv"}
    )