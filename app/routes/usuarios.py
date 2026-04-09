from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Usuario, RolEnum
from app.security import hash_password, require_admin

router = APIRouter()


class UsuarioCreate(BaseModel):
    username: str
    nombre: str
    password: str
    rol: RolEnum = RolEnum.empleado


class ActivoUpdate(BaseModel):
    activo: bool


@router.get("/")
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    return db.query(Usuario).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    if db.query(Usuario).filter(Usuario.username == data.username).first():
        raise HTTPException(status_code=400, detail="El username ya existe")

    user = Usuario(
        username=data.username,
        nombre=data.nombre,
        password_hash=hash_password(data.password),
        rol=data.rol
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{usuario_id}/activo")
def toggle_activo(
    usuario_id: int,
    data: ActivoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.activo = data.activo
    db.commit()
    db.refresh(user)
    return user