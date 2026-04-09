# 📦 OrderFlow — Sistema de Gestión de Pedidos

Sistema web para centralizar y gestionar pedidos de una tienda de reventa de ropa,
recibidos por WhatsApp y correo electrónico. Desarrollado como práctica de SDLC
completo con herramientas de IA generativa.

---

## 📚 Documentación del proyecto

| Documento | Descripción |
|-----------|-------------|
| [📋 Análisis funcional y requisitos](docs/01_Analisis_funcional_y_requisitos.md) | Actores, RF, RNF, restricciones y riesgos |
| [👤 Historias de usuario](docs/02_Historias_de_usuario.md) | Backlog completo con épicas y criterios de aceptación |
| [🛠️ Diseño técnico](docs/03_Diseno_tecnico_y_propuesta.md) | Arquitectura, stack, modelo de datos y API |
| [🧪 Plan de pruebas](docs/04_Plan_de_pruebas.md) | Casos de prueba, trazabilidad y resultados |
| [🧠 Decisiones técnicas](memory-bank/decisiones.md) | Memory bank con decisiones y deuda técnica |
| [🤖 Prompts utilizados](prompts/prompts_usados.md) | Prompts de Claude y Copilot usados en el proyecto |

---

## 🎯 Problema que resuelve

La tienda gestionaba los pedidos manualmente en Excel: un archivo activo y otro
histórico. Esto generaba riesgo de pérdida de datos, falta de visibilidad en
tiempo real y doble registro manual. OrderFlow centraliza todo en una única app web.

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.12 + FastAPI |
| Base de datos | SQLite (migrable a PostgreSQL) |
| ORM | SQLAlchemy |
| Autenticación | JWT (python-jose) + bcrypt |
| Backups | APScheduler |
| Tests | pytest + httpx |
| Frontend | HTML + Vanilla JS |

---

## ⚙️ Requisitos previos

- Python 3.11+
- pip
- Git

---

## 🚀 Instalación

    # 1. Clona el repositorio
    git clone https://github.com/TU_USUARIO/orderflow-genai.git
    cd orderflow-genai

    # 2. Crea el entorno virtual
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate

    # 3. Instala dependencias
    pip install -r requirements.txt

    # 4. Configura las variables de entorno
    cp .env.example .env
    # Edita .env y cambia JWT_SECRET por un valor seguro

    # 5. Crea el usuario administrador
    python create_admin.py

    # 6. Arranca el servidor
    uvicorn app.main:app --reload

La app estará disponible en http://127.0.0.1:8000
La documentación de la API en http://127.0.0.1:8000/docs

---

## 🔑 Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| JWT_SECRET | Secreto para firmar tokens JWT | cambia-esto-en-produccion |
| DATABASE_URL | URL de conexión a la base de datos | sqlite:///./orderflow.db |
| BACKUP_DIR | Directorio para los backups automáticos | ./backups |

---

## 📁 Estructura del proyecto

    orderflow-genai/
    ├── app/
    │   ├── main.py          # Entry point FastAPI
    │   ├── database.py      # Conexión y sesión SQLite
    │   ├── models.py        # Modelos SQLAlchemy (Pedido, Usuario)
    │   ├── security.py      # JWT, hash de contraseñas, dependencias auth
    │   ├── backup.py        # Scheduler de backups automáticos
    │   ├── routes/
    │   │   ├── auth.py      # POST /api/auth/login
    │   │   ├── pedidos.py   # CRUD /api/pedidos
    │   │   ├── historico.py # GET /api/historico
    │   │   └── usuarios.py  # /api/usuarios (solo admin)
    │   └── static/
    │       └── index.html   # Frontend Kanban
    ├── tests/
    │   ├── conftest.py      # Fixtures compartidos
    │   ├── test_auth.py
    │   ├── test_pedidos.py
    │   └── test_historico.py
    ├── docs/
    │   ├── 01_Analisis_funcional_y_requisitos.md
    │   ├── 02_Historias_de_usuario.md
    │   ├── 03_Diseno_tecnico_y_propuesta.md
    │   └── screenshots/
    ├── prompts/
    │   └── prompts_usados.md
    ├── create_admin.py
    ├── pytest.ini
    ├── requirements.txt
    └── .env.example

---

## 🧪 Tests

    # Ejecutar todos los tests
    pytest tests/ -v

    # Con reporte de cobertura
    pytest tests/ -v --cov=app --cov-report=term-missing

Resultado esperado: **18 passed** cubriendo autenticación, pedidos e histórico.

---

## 📋 Funcionalidades principales

- **Panel Kanban** con 3 columnas: Pendiente / En proceso / Enviado
- **Crear pedido** con cliente, artículo, talla, precio y canal (WhatsApp/email)
- **Cambiar estado** con un clic — al marcar como Enviado se archiva automáticamente
- **Histórico permanente** e inmutable de todos los pedidos enviados
- **Búsqueda** en el histórico por cliente o artículo
- **Exportar CSV** del histórico completo
- **Autenticación JWT** con roles admin/empleado
- **Backup automático** diario de la base de datos con rotación de 30 días

---

## 🤖 IA generativa utilizada

Este proyecto fue desarrollado como práctica de SDLC completo con IA:

| Fase | Herramienta |
|------|-------------|
| Análisis funcional y requisitos | Claude |
| Historias de usuario | Claude |
| Diseño técnico | Claude |
| Desarrollo del MVP | Claude + GitHub Copilot |
| Tests unitarios | Claude |
| Documentación | Claude |

Los prompts utilizados están disponibles en `/prompts/prompts_usados.md`.

---

## 📌 Próximos pasos

- [ ] Migración a PostgreSQL para entornos de producción
- [ ] Notificaciones por email al cambiar estado de pedido
- [ ] Dashboard con métricas y estadísticas de ventas
- [ ] Despliegue en Railway / Render
- [ ] Integración directa con WhatsApp Business API
