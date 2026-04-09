# 🤖 Prompts utilizados

## Herramienta: Claude (claude.ai)

### Análisis funcional, historias de usuario y diseño técnico
Generados en conversación interactiva describiendo el caso de negocio:
tienda de reventa de ropa con pedidos por WhatsApp y email, gestionados
en Excel con doble registro manual.

### Desarrollo del MVP
Generación iterativa de código FastAPI: modelos, rutas, autenticación JWT,
backup automático y frontend HTML/JS.

### Tests unitarios
Generación de 18 tests con pytest + httpx cubriendo auth, pedidos e histórico.
Cobertura de happy path, validaciones, casos límite y flujo completo de archivado.

### Corrección de errores
Resolución de: importaciones circulares, incompatibilidad passlib/Python 3.12,
configuración pytest con pythonpath.

---

## Herramienta: GitHub Copilot

Apoyo en autocompletado durante la implementación en VS Code,
especialmente en los modelos SQLAlchemy y los fixtures de pytest.