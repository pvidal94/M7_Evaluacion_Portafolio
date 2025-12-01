from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilFuncionario(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    CARGOS_MUNICIPALES = [
        ('ADMINISTRADOR', 'Administrador Municipal'),
        ('DAF', 'Director de Finanzas'),
        ('DIDECO', 'Director DIDECO'),
        ('CONTROL', 'Director de Control'),
        ('ALCALDE', 'Alcalde'),
        ('SECPLAN', 'SECPLAN - Planificación'),
        ('DOM', 'DOM - Obras'),
    ]
    
    cargo = models.CharField(max_length=50, choices=CARGOS_MUNICIPALES, default='DIDECO')
    es_jefe = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.user.username} ({self.cargo})"

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        PerfilFuncionario.objects.create(user=instance)
    instance.perfilfuncionario.save()

class CuentaPresupuestaria(models.Model):
    codigo_cuenta = models.CharField(max_length=50, unique=True, verbose_name="Código Presupuestario")
    nombre_cuenta = models.CharField(max_length=200, verbose_name="Nombre de la Cuenta")
    
    presupuesto_inicial = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Presupuesto Inicial")
    modificaciones = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Modificaciones Actuales")
    presupuesto_vigente = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Presupuesto Final Vigente")

    def __str__(self):
        return f"{self.codigo_cuenta} - {self.nombre_cuenta}"

class ComiteTecnico(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    miembros = models.ManyToManyField(User, related_name='comites_asignados')

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20, unique=True)
    director_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='proyectos_dirigidos')
    
    comites_revisores = models.ManyToManyField(ComiteTecnico, blank=True)

    def __str__(self):
        return f"[{self.codigo}] {self.nombre}"

class ActividadProyecto(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Completado', 'Completado'),
        ('Atrasado', 'Atrasado'),
    ]
    
    proyecto_padre = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='actividades_hijas', verbose_name="Proyecto Padre")
    
    activity_id = models.CharField(max_length=20, unique=True, verbose_name="ID Actividad")
    nombre_actividad = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tareas_asignadas') 
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"[{self.activity_id}] {self.nombre_actividad}"