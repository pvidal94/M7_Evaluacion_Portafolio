from django.contrib import admin
from django.urls import path
from gestion_municipal import views

urlpatterns = [
    # Administración y Autenticación
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Vistas de Contenido General
    path('dashboard/', views.dashboard, name='dashboard'),
    path('memoria-tecnica/', views.memoria_tecnica, name='memoria_tecnica'),
    
    # REQUERIMIENTO CRUD, ORM Y RELACIONES
    
    # 1. Leer (R) - Lista
    path('actividades/', views.lista_actividades, name='lista_actividades'),
    
    # 1.1. Leer (R) - Detalle de Entidad (Al hacer clic)
    # Se usa <int:pk> o <int:id> para la clave primaria de la actividad
    path('actividades/<int:pk>/', views.detalle_actividad, name='detalle_actividad'),
    
    # 2. Crear (C)
    path('actividades/nueva/', views.crear_actividad, name='crear_actividad'),
    
    # 3. Actualizar (U)
    path('actividades/editar/<int:id>/', views.editar_actividad, name='editar_actividad'),
    
    # 4. Eliminar (D)
    path('actividades/eliminar/<int:id>/', views.eliminar_actividad, name='eliminar_actividad'),

    # CONSULTA AVANZADA (ORM filter(), annotate())
    path('reporte/atrasos/', views.reporte_gestion, name='reporte_gestion'),
]