# 🛠️ Diseño Técnico y Propuesta Tecnológica
## OrderFlow — Sistema de Gestión de Pedidos

**Versión:** 1.0 | **Fecha:** Abril 2026  
**Herramienta IA usada:** Claude (diseño) + GitHub Copilot (implementación)

---

## 1. Arquitectura del sistema

**Patrón elegido: Monolito modular**

Justificación: equipo de un desarrollador, dominio simple y bien acotado,
tráfico bajo y predecible. No hay razón técnica que justifique microservicios.

    [Navegador — Chrome/Firefox/Safari]
               |  HTTP/S
               v
    [FastAPI App — Puerto 8000]
    +----------------------------------+
    | Router /api/auth                 |
    | Router /api/pedidos              |
    | Router /api/historico            |
    | Router /api/usuarios             |
    | Static /static (HTML + JS)       |
    +----------------------------------+
               |
               v
    [SQLite → PostgreSQL si escala]
    +----------------------------------+
    | Tabla: pedidos                   |
    | Tabla: usuarios                  |
    +----------------------------------+
               |
               v
    [/backups/ — copia diaria SQLite]

---

## 2. Stack tecnológico

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| Backend | Python 3.11 + FastAPI | Conocido por el dev, rápido, docs OpenAPI automáticas |
| Frontend | HTML + Vanilla JS | Sin build, funciona en cualquier navegador |
| Base de datos | SQLite (inicial) | 0 infraestructura, suficiente para el volumen esperado |
| ORM | SQLAlchemy + Alembic | Estándar Python, migraciones controladas |
| Autenticación | JWT (python-jose) + bcrypt | Stateless, simple con FastAPI, tokens de 8h |
| Backups | APScheduler + script Python | Backup automático sin infraestructura adicional |
| Tests | pytest + httpx | Estándar para APIs FastAPI |
| Hosting | Railway / Render (free tier) | Despliegue en minutos, sin coste inicial |

---

## 3. Modelo de datos

### Entidad: Pedido

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Autoincremental |
| cliente | String(100) | Nombre del cliente |
| articulo | String(200) | Descripción del artículo |
| talla | String(20) | Talla del artículo |
| precio | Float | Precio acordado |
| canal | Enum('whatsapp','email') | Canal de origen |
| estado | Enum('pendiente','en_proceso','enviado') | Estado actual |
| fecha_creacion | DateTime | Auto al crear |
| fecha_envio | DateTime (nullable) | Se registra al pasar a 'enviado' |
| creado_por | FK → Usuario.id | Usuario que creó el pedido |

### Entidad: Usuario

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Autoincremental |
| username | String(50) UNIQUE | Identificador de login |
| nombre | String(100) | Nombre visible |
| password_hash | String | Hash bcrypt |
| rol | Enum('admin','empleado') | Nivel de acceso |
| activo | Boolean | False = no puede entrar |

### Relaciones
- Pedido.creado_por → Usuario (N:1)
- El histórico NO es una tabla separada: son los pedidos con estado='enviado'

---

## 4. Diseño de API REST

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | /api/auth/login | Login, devuelve JWT | No |
| POST | /api/auth/logout | Invalida token | Sí |
| GET | /api/pedidos | Lista pedidos activos (?estado=) | Sí |
| POST | /api/pedidos | Crea nuevo pedido | Sí |
| PUT | /api/pedidos/{id} | Edita pedido activo | Sí |
| PATCH | /api/pedidos/{id}/estado | Cambia estado | Sí |
| GET | /api/historico | Lista pedidos enviados (?q=) | Sí |
| GET | /api/historico/export | Descarga CSV | Sí (admin) |
| GET | /api/usuarios | Lista usuarios | Sí (admin) |
| POST | /api/usuarios | Crea usuario | Sí (admin) |
| PATCH | /api/usuarios/{id}/activo | Activa/desactiva | Sí (admin) |

---

## 5. Estructura de carpetas del proyecto

    orderflow-genai/
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── auth.py
    │   ├── backup.py
    │   ├── routes/
    │   │   ├── auth.py
    │   │   ├── pedidos.py
    │   │   ├── historico.py
    │   │   └── usuarios.py
    │   └── static/
    │       └── index.html
    ├── tests/
    │   ├── conftest.py
    │   ├── test_auth.py
    │   ├── test_pedidos.py
    │   └── test_historico.py
    ├── docs/
    │   ├── 01_Analisis_funcional_y_requisitos.md
    │   ├── 02_Historias_de_usuario.md
    │   ├── 03_Diseno_tecnico_y_propuesta.md
    │   ├── 04_Plan_de_pruebas.md
    │   └── screenshots/
    ├── prompts/
    │   └── prompts_usados.md
    ├── memory-bank/
    │   └── decisiones.md
    ├── backups/
    ├── .env.example
    ├── requirements.txt
    └── README.md

---

## 6. Seguridad

- **Autenticación:** JWT firmado con secreto en variable de entorno, expira 8h
- **Contraseñas:** Hash bcrypt (coste 12), nunca texto plano
- **Autorización:** Middleware verifica token en todas las rutas protegidas
- **Roles:** Rutas de admin verifican rol adicional
- **CORS:** Solo acepta el dominio de la app en producción
- **Variables de entorno:** JWT_SECRET y DATABASE_URL en .env (nunca en git)
- **Backups:** Copia SQLite a /backups/ con rotación de 30 días

---

## 7. Estimación de esfuerzo

| Fase | Contenido | Duración |
|------|-----------|----------|
| Setup | Estructura, modelos, DB, auth | 3-4 días |
| MVP pedidos | CRUD, cambio estado, archivado | 4-5 días |
| Frontend | Panel HTML/JS, formulario, filtros | 3-4 días |
| Histórico + backups | Vista, búsqueda, CSV, scheduler | 2-3 días |
| Tests | pytest, cobertura >70% | 2-3 días |
| Despliegue | Railway/Render, variables, pruebas | 1-2 días |

**Total estimado: 4-6 semanas a tiempo parcial**