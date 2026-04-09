# 👤 Historias de Usuario — Product Backlog
## OrderFlow — Sistema de Gestión de Pedidos

**Versión:** 1.0 | **Fecha:** Abril 2026  
**Herramienta IA usada:** Claude

---

## Épica 1 — Autenticación y acceso

---

**US-001 · Login de usuario**
Como empleado o propietario,
quiero iniciar sesión con usuario y contraseña,
para acceder al sistema de forma segura.

**Criterios de aceptación:**
- CA-1: El sistema muestra formulario con campos usuario y contraseña
- CA-2: Con credenciales correctas accedo al panel principal
- CA-3: Con credenciales incorrectas aparece error sin revelar qué campo falló
- CA-4: El token expira a las 8 horas y redirige al login

**Estimación:** S | **Prioridad:** Must | **Dependencias:** Ninguna

---

**US-002 · Cierre de sesión**
Como usuario autenticado,
quiero cerrar sesión desde cualquier pantalla,
para proteger el acceso en dispositivos compartidos.

**Criterios de aceptación:**
- CA-1: Botón de logout visible en todo momento
- CA-2: Al cerrar sesión el token se invalida y redirige al login

**Estimación:** XS | **Prioridad:** Must | **Dependencias:** US-001

---

**US-003 · Gestión de usuarios (admin)**
Como propietario,
quiero crear y desactivar cuentas de empleados,
para controlar quién puede acceder al sistema.

**Criterios de aceptación:**
- CA-1: Puedo crear usuario con nombre, username y contraseña
- CA-2: Puedo desactivar un usuario sin eliminarlo
- CA-3: Un usuario desactivado no puede iniciar sesión

**Estimación:** S | **Prioridad:** Should | **Dependencias:** US-001

---

## Épica 2 — Gestión de pedidos activos

---

**US-004 · Ver panel de pedidos**
Como empleado,
quiero ver todos los pedidos agrupados por estado,
para saber en todo momento qué hay pendiente, en proceso y enviado.

**Criterios de aceptación:**
- CA-1: El panel muestra 3 secciones: Pendiente / En proceso / Enviado
- CA-2: Cada pedido muestra: cliente, artículo, talla, precio, canal y fecha
- CA-3: Hay un contador de pedidos por sección
- CA-4: La vista se actualiza sin recargar la página

**Estimación:** M | **Prioridad:** Must | **Dependencias:** US-001

---

**US-005 · Crear nuevo pedido**
Como empleado,
quiero registrar un nuevo pedido con todos sus datos,
para no tener que usar Excel y centralizar la información.

**Criterios de aceptación:**
- CA-1: Formulario con campos obligatorios: cliente, artículo, talla, precio, canal
- CA-2: El pedido se crea con estado "Pendiente" por defecto
- CA-3: La fecha de creación se registra automáticamente
- CA-4: El pedido aparece en el panel inmediatamente

**Estimación:** S | **Prioridad:** Must | **Dependencias:** US-004

---

**US-006 · Cambiar estado de pedido**
Como empleado,
quiero cambiar el estado de un pedido con un clic,
para reflejar su progreso en tiempo real.

**Criterios de aceptación:**
- CA-1: Cada pedido tiene un control para cambiar entre los 3 estados
- CA-2: Al pasar a "Enviado" el pedido desaparece del panel activo
- CA-3: El pedido archivado aparece en el histórico con fecha de envío

**Estimación:** S | **Prioridad:** Must | **Dependencias:** US-004, US-005

---

**US-007 · Editar pedido activo**
Como empleado,
quiero corregir los datos de un pedido antes de enviarlo,
para rectificar errores de entrada.

**Criterios de aceptación:**
- CA-1: Todos los campos son editables excepto la fecha de creación
- CA-2: Los pedidos del histórico (Enviado) no son editables

**Estimación:** S | **Prioridad:** Should | **Dependencias:** US-005

---

**US-008 · Filtrar pedidos por estado**
Como empleado,
quiero filtrar el panel por estado,
para centrarme en los pedidos que me corresponde gestionar.

**Criterios de aceptación:**
- CA-1: Filtros visibles: Todos / Pendiente / En proceso / Enviado
- CA-2: El filtro activo se resalta visualmente

**Estimación:** XS | **Prioridad:** Should | **Dependencias:** US-004

---

## Épica 3 — Histórico de pedidos

---

**US-009 · Ver histórico**
Como propietario,
quiero ver el historial completo de todos los pedidos enviados,
para tener trazabilidad total del negocio.

**Criterios de aceptación:**
- CA-1: Sección separada accesible desde el menú principal
- CA-2: Muestra fecha de creación y fecha de envío
- CA-3: Ordenado por fecha de envío descendente

**Estimación:** S | **Prioridad:** Must | **Dependencias:** US-006

---

**US-010 · Buscar en el histórico**
Como propietario,
quiero buscar pedidos por nombre de cliente o artículo,
para encontrar un pedido concreto rápidamente.

**Criterios de aceptación:**
- CA-1: Campo de búsqueda libre que filtra en tiempo real
- CA-2: Filtra por cliente y por artículo simultáneamente

**Estimación:** XS | **Prioridad:** Should | **Dependencias:** US-009

---

**US-011 · Exportar histórico a CSV**
Como propietario,
quiero descargar el histórico en CSV,
para analizarlo externamente o guardarlo como backup legible.

**Criterios de aceptación:**
- CA-1: Botón de exportación en la vista de histórico
- CA-2: CSV incluye todas las columnas con cabeceras en español

**Estimación:** XS | **Prioridad:** Could | **Dependencias:** US-009

---

## Épica 4 — Seguridad y backups

---

**US-012 · Backup automático diario**
Como propietario,
quiero que el sistema haga copias de seguridad automáticas,
para no perder ningún pedido aunque haya un fallo.

**Criterios de aceptación:**
- CA-1: Backup de la BBDD cada 24 horas con nombre que incluye la fecha
- CA-2: Se mantienen los últimos 30 backups (rotación automática)

**Estimación:** S | **Prioridad:** Must | **Dependencias:** Ninguna

---

## Resumen del backlog

| Épica | Historias | Story Points | Prioridad mínima |
|-------|-----------|-------------|-----------------|
| Autenticación | US-001 a US-003 | 7 SP | Must |
| Pedidos activos | US-004 a US-008 | 13 SP | Must |
| Histórico | US-009 a US-011 | 6 SP | Must / Could |
| Seguridad | US-012 | 3 SP | Must |
| **Total** | **12 historias** | **29 SP** | |