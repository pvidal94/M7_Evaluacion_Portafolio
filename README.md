# 🏛️ Dashboard de Gestión Municipal: Ilustre Municipalidad de Puyehue

**Proyecto de Portafolio Web Desarrollado por Patricia VIdal Uribe**

Este sistema es una aplicación integrada para el seguimiento de la gestión y el control de presupuesto, desarrollado íntegramente con el framework **Django**. Demuestra dominio en desarrollo Full Stack, arquitectura MVT y la implementación de un robusto control de acceso basado en roles (RBAC).

## 🚀 Arquitectura y Tecnologías Clave

El proyecto cumple con los estándares de aplicaciones empresariales al usar la arquitectura "baterías incluidas" de Django.

| Componente | Tecnología | Evidencia del Dominio |
| :--- | :--- | :--- |
| **Backend** | Python 3.11, **Django 4.x** | Lógica de negocio, ORM, Autenticación y Seguridad (CSRF, SQL Injection). |
| **Seguridad** | **RBAC** (Roles y Permisos) | Segregación de Funciones (SoD) entre DAF y Administración Municipal. |
| **Frontend** | HTML, DTL, **Bootstrap 5** | Interfaz dinámica, responsiva, y aplicación de plantillas para contenido (`lista_actividades.html`). |
| **Gestión de Código** | **Management Commands** | Scripts de gestión (`poblar_datos_base.py`) para automatizar la carga inicial de usuarios y datos. |

---

## 🔒 Control de Acceso y Roles (RBAC)

Se implementó el módulo `django.contrib.auth` con una estructura de grupos que simula la jerarquía municipal. Todas las vistas están protegidas con el decorador `@login_required`.

| Rol | Usuario | Contraseña | Permisos Exclusivos (Backend) |
| :--- | :--- | :--- | :--- |
| **Administrador Municipal** | `administrador_municipal` | `TheStrokes94.` | **Full Control (C/E/D)** sobre Actividades. |
| **Director de Finanzas (DAF)** | `director_finanzas` | `TheStrokes94.` | **Modificar/Crear** Cuentas Presupuestarias (Solo en `/admin`). |
| **Directores Lectura** | `dideco`, `alcalde` | `TheStrokes94.` | **Solo Visualización** (Read Only) en el Dashboard y Actividades. |

---

## 🛠️ Guía de Ejecución Rápida

Sigue estos pasos en la terminal de tu proyecto para levantar la aplicación:

1.  **Clonar Repositorio:**
    ```bash
    git clone [https://github.com/pvidal94/M6_Portafolio](https://github.com/pvidal94/M6_Portafolio)
    cd M6_Portafolio
    ```

2.  **Configurar Entorno Virtual e Instalar Django:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # O source venv/bin/activate en Linux/Mac
    pip install django
    ```

3.  **Preparar Base de Datos y Cargar Datos Iniciales (Usuarios y Presupuesto):**

    ```bash
    # Aplicar todas las migraciones de modelos
    python manage.py makemigrations gestion_municipal
    python manage.py migrate
    
    # Carga automática de usuarios y datos ficticios de presupuesto ($2.350M)
    python manage.py poblar_datos_base
    ```

4.  **Iniciar Servidor:**
    ```bash
    python manage.py runserver
    ```
    Accede a la aplicación en `http://127.0.0.1:8000/`.

---
### 🎯 Características Destacadas

* **Memoria Técnica Integrada:** Incluye una pestaña "Memoria Técnica" que explica la arquitectura del proyecto *in-situ*, cumpliendo los requerimientos de documentación académica.
* **Gestión de Presupuesto:** El usuario `director_finanzas` es el único autorizado a modificar los campos `Presupuesto Inicial`, `Modificaciones` y `Presupuesto Vigente` a través del panel de administración.

Rol	Usuario	Propósito de Seguridad	Permisos Exclusivos
Administrador Municipal	administrador_municipal	Controla la ejecución del proyecto y los reportes de avance.	🔨 Control Total (Crear, Editar, Eliminar) sobre Actividades.

Director de Finanzas (DAF)	director_finanzas	Responsable del control presupuestario y flujo de caja.	💰 Modificación/Creación de Cuentas Presupuestarias (Solo en /admin).

Directores Lectura	dideco, alcalde, director_control	Monitoreo y Supervisión del estado general de la municipalidad.	👀 Solo Visualización (Lectura) en el Dashboard y Actividades.

Contraseña para todos los perfiles de prueba: TheStrokes94.
