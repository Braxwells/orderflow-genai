# 🧪 Plan de Pruebas
## OrderFlow — Sistema de Gestión de Pedidos

**Versión:** 1.0 | **Fecha:** Abril 2026  
**Herramienta IA usada:** Claude

---

## 1. Objetivo

Verificar que el sistema OrderFlow cumple los requisitos funcionales definidos,
con especial atención a la integridad del histórico de pedidos (dato crítico
para el negocio) y la seguridad de acceso mediante JWT.

---

## 2. Alcance

| Incluido | Excluido |
|----------|----------|
| API REST completa (pedidos, histórico, auth, usuarios) | Tests de rendimiento a gran escala |
| Flujo completo de archivado al histórico | Tests E2E de navegador |
| Autenticación y autorización JWT | Tests de la interfaz visual |
| Validaciones de campos obligatorios | Integración con WhatsApp/email |

---

## 3. Tipos de prueba

| Tipo | Herramienta | Cobertura objetivo | Estado |
|------|-------------|-------------------|--------|
| Integración API | pytest + httpx TestClient | 100% endpoints críticos | ✅ Implementado |
| Unitario (lógica) | pytest | Cambio de estado, archivado | ✅ Implementado |
| Validación de entrada | pytest | Campos obligatorios, tipos | ✅ Implementado |
| Seguridad básica | pytest | Auth, roles, tokens | ✅ Implementado |
| Manual exploratorio | Navegador | Flujos UI principales | ✅ Realizado |

---

## 4. Casos de prueba

### Módulo: Autenticación

| ID | Caso | Resultado esperado | Estado |
|----|------|--------------------|--------|
| TC-001 | Login con credenciales correctas | 200 + token JWT | ✅ PASS |
| TC-002 | Login con contraseña incorrecta | 401, mensaje genérico | ✅ PASS |
| TC-003 | Login con usuario inexistente | 401 | ✅ PASS |
| TC-004 | Acceso a ruta protegida sin token | 401 | ✅ PASS |
| TC-005 | Acceso con token inválido/falso | 401 | ✅ PASS |

### Módulo: Pedidos

| ID | Caso | Resultado esperado | Estado |
|----|------|--------------------|--------|
| TC-006 | Crear pedido con datos válidos | 201 + pedido en estado pendiente | ✅ PASS |
| TC-007 | Crear pedido sin campo cliente | 422 Validation Error | ✅ PASS |
| TC-008 | Crear pedido sin campo precio | 422 Validation Error | ✅ PASS |
| TC-009 | Listar pedidos activos | 200 + lista sin enviados | ✅ PASS |
| TC-010 | Cambiar estado a en_proceso | 200 + estado actualizado | ✅ PASS |
| TC-011 | Cambiar estado a enviado | 200 + fecha_envio registrada | ✅ PASS |
| TC-012 | Pedido enviado desaparece de activos | No aparece en GET /pedidos | ✅ PASS |
| TC-013 | Pedido enviado aparece en histórico | Aparece en GET /historico | ✅ PASS |
| TC-014 | Editar pedido activo | 200 + datos actualizados | ✅ PASS |
| TC-015 | Editar pedido del histórico | 403 Forbidden | ✅ PASS |
| TC-016 | Cambiar estado de pedido inexistente | 404 Not Found | ✅ PASS |

### Módulo: Histórico

| ID | Caso | Resultado esperado | Estado |
|----|------|--------------------|--------|
| TC-017 | Histórico vacío inicial | 200 + lista vacía | ✅ PASS |
| TC-018 | Histórico contiene pedido enviado | Pedido presente en lista | ✅ PASS |
| TC-019 | Búsqueda por nombre de cliente | Filtra correctamente | ✅ PASS |
| TC-020 | Búsqueda sin resultados | 200 + lista vacía | ✅ PASS |

---

## 5. Trazabilidad con historias de usuario

| Test | Historia de usuario |
|------|---------------------|
| TC-001 a TC-005 | US-001, US-002 |
| TC-006 a TC-009 | US-004, US-005 |
| TC-010 a TC-013 | US-006 |
| TC-014 a TC-015 | US-007 |
| TC-017 a TC-020 | US-009, US-010 |

---

## 6. Resultado de ejecución

    pytest tests/ -v
    ======================== 18 passed in 7.32s ========================

Cobertura de los módulos críticos (pedidos, auth, histórico): > 80%

---

## 7. Criterios de aceptación del sistema

- 18/18 tests pasan al 100%
- Cero bugs críticos abiertos
- El flujo completo (crear → procesar → enviar → histórico) funciona sin errores
- Los pedidos del histórico no pueden modificarse
- El sistema rechaza accesos sin token válido

---

## 8. Gestión de defectos

| Severidad | Descripción | SLA resolución |
|-----------|-------------|----------------|
| Crítico | Pérdida de datos o histórico inaccesible | 4 horas |
| Alto | No se puede crear o cambiar estado | 24 horas |
| Medio | Búsqueda o filtros incorrectos | 72 horas |
| Bajo | Problema visual o de formato | Siguiente sesión |