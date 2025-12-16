#  Tienda 3D & Deco - Backend Django

Sistema de gestión de pedidos e inventario para una tienda de productos personalizados e impresión 3D. Desarrollado en Django 5 con Django REST Framework.

## 📋Características

* **Catálogo Web:** Vista de productos y formulario de pedidos.
* **Tracking:** Sistema de seguimiento de pedidos mediante Token.
* **Panel Administrativo:** Dashboard con gráficos (Chart.js) para métricas de ventas.
* **API REST:** Endpoints para integración con sistemas externos.

##  Despliegue

Este proyecto está configurado para desplegarse en **Render**.

* **URL del Proyecto:** (: https://tienda-backend.onrender.com)
* **Usuario Admin:** `admin`
* **Contraseña:** `admin123`

##  Endpoints de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/insumos/` | Listar insumos |
| `POST` | `/api/pedidos/crear/` | Crear nuevo pedido |
| `GET` | `/api/pedidos/filtrar/` | Filtrar pedidos por fecha/estado |
| `GET` | `/reporte/` | Dashboard de gráficos (Requiere Login) |

---
**Asignatura:** programación web