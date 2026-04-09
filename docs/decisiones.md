# 🧠 Memory Bank — Decisiones técnicas

## OrderFlow | Abril 2026

---

## D-001 — No crear tabla separada para el histórico

**Decisión:** El histórico no es una tabla separada. Son los pedidos
con estado='enviado'.

**Razón:** Simplifica la arquitectura, elimina el paso manual de
copiar entre tablas (que era exactamente el problema del Excel),
y garantiza que ningún pedido se pierda en la transición.

**Alternativa descartada:** Tabla `historico` separada con INSERT
al archivar y DELETE en pedidos activos — demasiado riesgo de
inconsistencia si falla a mitad.

---

## D-002 — SQLite en lugar de PostgreSQL para el inicio

**Decisión:** SQLite como base de datos inicial.

**Razón:** Volumen de pedidos bajo y predecible. Cero infraestructura
adicional. Facilita el despliegue en Railway/Render sin configurar
una BD externa.

**Plan de migración:** SQLAlchemy abstrae la BD — cambiar
DATABASE_URL en .env es suficiente para migrar a PostgreSQL
cuando sea necesario.

---

## D-003 — bcrypt directo en lugar de passlib

**Decisión:** Usar la librería `bcrypt` directamente en lugar de
`passlib[bcrypt]`.

**Razón:** `passlib` tiene un bug de compatibilidad con Python 3.12
— usa el módulo `crypt` que fue eliminado en esa versión. `bcrypt`
directo funciona correctamente y sin dependencias problemáticas.

---

## D-004 — Renombrar auth.py a security.py

**Decisión:** El módulo de utilidades JWT se llama `security.py`,
no `auth.py`.

**Razón:** Existía conflicto de nombres con `app/routes/auth.py`.
Python interpretaba imports circulares al tener dos módulos
llamados `auth` en el mismo paquete.

---

## D-005 — Frontend en Vanilla JS sin framework

**Decisión:** HTML + JavaScript puro, sin React ni Vue.

**Razón:** El proyecto es una práctica académica con un único
desarrollador. Sin herramientas de build, sin dependencias de
Node, desplegable directamente como archivos estáticos de FastAPI.

---

## Deuda técnica conocida

- `datetime.utcnow()` → migrar a `datetime.now(timezone.utc)` en todos los modelos
- CORS configurado con `allow_origins=["*"]` — restringir al dominio real en producción
- Sin paginación en el histórico — necesaria si el volumen crece
- Sin tests del frontend (solo API)
- Backup almacenado localmente — mover a S3 o Google Drive en producción