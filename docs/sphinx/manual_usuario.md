# 📘 Manual de Usuario — Task & Client Manager

Sistema de escritorio para la gestión de clientes, tareas y reuniones.

---

## Índice

1. [Inicio de la aplicación](#1-inicio-de-la-aplicación)
2. [Panel de Clientes](#2-panel-de-clientes)
   - [Agregar cliente](#21-agregar-cliente)
   - [Editar cliente](#22-editar-cliente)
   - [Eliminar cliente](#23-eliminar-cliente)
   - [Buscar cliente](#24-buscar-cliente)
   - [Seleccionar cliente](#25-seleccionar-cliente)
3. [Panel de Tareas](#3-panel-de-tareas)
   - [Agregar tarea](#31-agregar-tarea)
   - [Editar tarea](#32-editar-tarea)
   - [Eliminar tarea](#33-eliminar-tarea)
4. [Panel de Reuniones](#4-panel-de-reuniones)
   - [Agregar reunión](#41-agregar-reunión)
   - [Editar reunión](#42-editar-reunión)
   - [Eliminar reunión](#43-eliminar-reunión)
   - [Colores según estado de pago](#44-colores-según-estado-de-pago)
5. [Calendario emergente](#5-calendario-emergente)
6. [Ordenamiento de tablas](#6-ordenamiento-de-tablas)
7. [Tooltips](#7-tooltips)
8. [Solución de problemas](#8-solución-de-problemas)

---

## 1. Inicio de la aplicación

Ejecutar en la terminal:

```bash
python main.py
```

La aplicación se abre maximizada con tres paneles principales:

```
┌──────────────────────────────────────────────────┐
│                   CLIENTES                        │
│  [Formulario]  [Botones: Add, Edit, Delete...]   │
│  [Tabla de clientes]                              │
├──────────────────────┬───────────────────────────┤
│    CLIENT TASKS      │    CLIENT MEETINGS         │
│  [Formulario]        │  [Formulario]              │
│  [Tabla de tareas]   │  [Tabla de reuniones]      │
└──────────────────────┴───────────────────────────┘
```

---

## 2. Panel de Clientes

### 2.1 Agregar cliente

1. Completar los campos del formulario:
   - **First Name** (obligatorio — solo letras y espacios)
   - **Last Name** (obligatorio — solo letras y espacios)
   - **Email** (obligatorio — formato email válido)
   - **Phone** (obligatorio — 6 a 20 dígitos, acepta +, -, (), espacios)
   - **Company** (opcional)
   - **Category** (seleccionar: Client, Lead, VIP, Active, Inactive, Prospect)
   - **Source** (seleccionar: Website, Referral, Instagram, LinkedIn, Email, Event, Other)
   - **Preferred** (seleccionar método de contacto preferido)
2. Hacer clic en **"Add Client"**
3. Si la validación es correcta, el cliente se agrega y se selecciona automáticamente en la tabla

### 2.2 Editar cliente

1. Seleccionar un cliente en la tabla
2. Hacer clic en **"Edit Client"**
3. En la ventana emergente, modificar los campos necesarios
4. Hacer clic en **"Save"** para guardar o **"Cancel"** para descartar

### 2.3 Eliminar cliente

1. Seleccionar un cliente en la tabla
2. Hacer clic en **"Delete Client"**
3. Confirmar la eliminación en el cuadro de diálogo
4. **Importante:** se eliminan también todas sus tareas y reuniones asociadas

### 2.4 Buscar cliente

1. Escribir texto en el campo **"Search"**
2. Presionar **Enter** o hacer clic en **"Search"**
3. La tabla se filtra mostrando solo los clientes que coinciden en cualquier campo
4. Para volver a ver todos, borrar el texto y presionar **Enter** o **"Search"**

### 2.5 Seleccionar cliente

- Hacer clic en cualquier fila de la tabla de clientes
- O seleccionar la fila y hacer clic en **"Select Client"**
- Al seleccionar un cliente, los paneles de tareas y reuniones se cargan automáticamente con sus datos

---

## 3. Panel de Tareas

### 3.1 Agregar tarea

1. Tener un cliente seleccionado
2. Completar los campos:
   - **Task** (obligatorio — descripción de la tarea)
   - **Status** (seleccionar: Pending, In Progress, Completed)
   - **Start** (fecha de inicio)
   - **Deadline** (fecha límite)
3. Hacer clic en **"New Task"**
4. Las fechas no se validan si el estado es "Completed"

### 3.2 Editar tarea

1. Hacer doble clic en una tarea de la tabla (o seleccionarla y modificar los campos manualmente)
2. Los datos de la tarea se copian al formulario
3. Modificar los campos necesarios
4. Hacer clic en **"Edit"**

### 3.3 Eliminar tarea

1. Seleccionar una tarea en la tabla (hacer clic en la fila)
2. Hacer clic en **"Delete"**
3. Confirmar la eliminación

---

## 4. Panel de Reuniones

### 4.1 Agregar reunión

1. Tener un cliente seleccionado
2. Completar los campos:
   - **Meeting** (obligatorio — descripción)
   - **Date** (fecha de la reunión)
   - **Payment** (estado de pago)
   - **Date Pay** (fecha de pago — solo si el estado es "Paid")
   - **Total** (monto total)
   - **Paid** (monto pagado)
   - **Method** (método de pago)
3. Hacer clic en **"New Meeting"**

**Reglas de validación:**
- Si el estado es **"Paid"**: Date Pay es obligatoria y no puede ser futura; si Paid está vacío se iguala a Total
- Si el estado es **distinto de "Paid"**: Date Pay no debe ingresarse
- Paid no puede ser mayor que Total

### 4.2 Editar reunión

1. Hacer doble clic en una reunión de la tabla
2. Los datos se copian al formulario
3. Modificar los campos necesarios
4. Hacer clic en **"Edit"**

### 4.3 Eliminar reunión

1. Seleccionar una reunión en la tabla
2. Hacer clic en **"Delete"**
3. Confirmar la eliminación

### 4.4 Colores según estado de pago

| Estado | Color |
|--------|-------|
| Paid | Verde claro |
| Unpaid | Rojo claro |
| Pending | Amarillo claro |
| Overdue | Rojo intenso |
| Partially Paid | Naranja claro |
| Refunded | Azul claro |
| Cancelled | Gris claro |

---

## 5. Calendario emergente

Los campos de fecha tienen un botón **📅** a su derecha.

1. Hacer clic en **📅**
2. Navegar entre meses con las flechas **◀** y **▶**
3. Hacer clic en el día deseado
4. Presionar **"Aceptar"** para insertar la fecha o **"Cancelar"** para cerrar

Formato de fecha: `DD/MM/YYYY` (también acepta `YYYY-MM-DD`)

---

## 6. Ordenamiento de tablas

Hacer clic en el encabezado de cualquier columna para ordenar:

- **Primer clic:** orden ascendente (▲)
- **Segundo clic:** orden descendente (▼)
- **Tercer clic:** vuelve a ascendente

Las tablas de clientes y tareas tienen formato zebra (filas alternadas).

---

## 7. Tooltips

Al pasar el cursor sobre celdas con texto largo (Email, Company, Task, Meeting, etc.), aparece un globo emergente con el contenido completo.

---

## 8. Solución de problemas

| Problema | Causa posible | Solución |
|----------|---------------|----------|
| La app no abre | Falta CustomTkinter | `pip install customtkinter` |
| Error de base de datos | Permisos en carpeta data | Verificar que la carpeta `data/` tenga permisos de escritura |
| La ventana se ve cortada | DPI scaling en Windows | La app ajusta automáticamente el DPI al iniciar |
| No se ven las tablas | Cliente no seleccionado | Seleccionar un cliente en el panel superior |
| Fechas no se guardan | Formato incorrecto | Usar DD/MM/AAAA o seleccionar con el calendario |

---

*Documentación generada para el proyecto final de la Diplomatura en Python — UTN*
