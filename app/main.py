import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.backup import start_backup_scheduler
from app.routes import auth, pedidos, historico, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_backup_scheduler()
    yield


app = FastAPI(
    title="OrderFlow API",
    description="Sistema de gestión de pedidos para tienda de reventa de ropa",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/api/auth",      tags=["Auth"])
app.include_router(pedidos.router,   prefix="/api/pedidos",   tags=["Pedidos"])
app.include_router(historico.router, prefix="/api/historico", tags=["Histórico"])
app.include_router(usuarios.router,  prefix="/api/usuarios",  tags=["Usuarios"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")