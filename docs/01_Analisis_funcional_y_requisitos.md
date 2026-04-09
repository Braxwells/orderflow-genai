# 📋 Análisis Funcional y Requisitos
## OrderFlow — Sistema de Gestión de Pedidos

**Proyecto:** OrderFlow  
**Versión:** 1.0  
**Fecha:** Abril 2026  
**Dominio:** Comercio / Reventa de ropa  
**Herramienta IA usada:** Claude (análisis) + GitHub Copilot (desarrollo)

---

## 1. Contexto del negocio

Distribuciones OrderFlow es una tienda de reventa de ropa que recibe pedidos
de clientes a través de WhatsApp y correo electrónico. El proceso actual es
manual: los pedidos se registran en Excel, se preparan por orden de llegada,
se envían por tandas y se archivan en una segunda hoja de cálculo.

**Problemas actuales:**
- No hay visibilidad compartida en tiempo real entre el equipo
- El doble registro (Excel activo → Excel histórico) es propenso a errores
- Riesgo de pérdida de pedidos al borrarlos manualmente del Excel activo

---

## 2. Objetivo del sistema

Centralizar la gestión de pedidos en una aplicación web accesible desde
cualquier navegador, que permita crear pedidos, cambiar su estado y mantener
un histórico permanente sin riesgo de pérdida de datos.

---

## 3. Actores del sistema

| Actor | Descripción | Permisos |
|-------|-------------|----------|
| Propietario (Admin) | Dueño del negocio | CRUD completo, gestión de usuarios, exportar CSV |
| Empleado | Personal de tienda | Crear pedidos, ver todos, cambiar estado |

---

## 4. Requisitos Funcionales

| ID | Descripción | Prioridad | Actor |
|----|-------------|-----------|-------|
| RF-001 | Ver todos los pedidos agrupados por estado (Pendiente / En proceso / Enviado) | Must | Todos |
| RF-002 | Crear pedido con: cliente, artículo, talla, precio, canal (WhatsApp/email) | Must | Todos |
| RF-003 | Cambiar estado de un pedido entre Pendiente, En proceso y Enviado | Must | Todos |
| RF-004 | Al marcar como Enviado, archivar automáticamente en el histórico | Must | Sistema |
| RF-005 | Mantener histórico permanente e inmutable de pedidos enviados | Must | Sistema |
| RF-006 | Mostrar canal de origen (WhatsApp/email) en el listado | Must | Todos |
| RF-007 | Filtrar pedidos por estado | Should | Todos |
| RF-008 | Buscar en el histórico por nombre de cliente | Should | Todos |
| RF-009 | Editar datos de un pedido activo (no del histórico) | Should | Todos |
| RF-010 | Registrar fecha y hora de creación automáticamente | Must | Sistema |
| RF-011 | Registrar fecha de envío al archivar | Must | Sistema |
| RF-012 | Autenticación con usuario y contraseña (JWT) | Must | Todos |
| RF-013 | Gestión de usuarios por parte del admin | Should | Admin |
| RF-014 | Exportar histórico a CSV | Could | Admin |
| RF-015 | Backup automático diario de la base de datos | Must | Sistema |

---

## 5. Requisitos No Funcionales

| ID | Categoría | Descripción | Métrica |
|----|-----------|-------------|---------|
| RNF-001 | Rendimiento | Carga del listado de pedidos | < 1 segundo |
| RNF-002 | Disponibilidad | Uptime del sistema | > 99% mensual |
| RNF-003 | Seguridad | Contraseñas con hash bcrypt | Sin texto plano |
| RNF-004 | Seguridad | Rutas protegidas con JWT | Token expira en 8h |
| RNF-005 | Persistencia | Backup automático de la BBDD | 1 backup/día, 30 días |
| RNF-006 | Usabilidad | Accesible desde navegador de escritorio y móvil | Sin instalación cliente |
| RNF-007 | Mantenibilidad | Código documentado con docstrings | Cobertura tests > 70% |

---

## 6. Restricciones

- Sin integración directa con WhatsApp API ni cliente de correo (registro manual)
- Sin pasarela de pago en este alcance
- Mantenible por un único desarrollador (perfil Python/FastAPI)
- Hosting de bajo coste: Railway / Render / VPS básico

---

## 7. Riesgos identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Pérdida de datos por fallo sin backup | Baja | Alto | Backup diario + copia manual semanal |
| No adopción por el equipo | Media | Alto | UI minimalista, onboarding < 15 min |
| SQLite insuficiente si escala | Baja | Medio | Migración a PostgreSQL preparada con SQLAlchemy |

---

## 8. Criterios de aceptación de alto nivel

- El equipo puede crear y cambiar estado de pedidos sin usar Excel
- Ningún pedido enviado puede perderse o editarse desde el histórico
- El sistema arranca y es usable en < 15 minutos por un empleado nuevo
- Los tests unitarios pasan al 100% en CI