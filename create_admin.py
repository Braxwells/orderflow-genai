from app.database import init_db, SessionLocal
from app.models import Usuario, RolEnum
from app.security import hash_password

init_db()
db = SessionLocal()

admin = Usuario(
    username="admin",
    nombre="Administrador",
    password_hash=hash_password("admin123"),
    rol=RolEnum.admin,
    activo=True
)
db.add(admin)
db.commit()
print("✅ Usuario admin creado — username: admin / password: admin123")
db.close()