import csv
from datetime import date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion_municipal.models import ActividadProyecto, CuentaPresupuestaria, Proyecto

class Command(BaseCommand):
    help = 'Carga usuarios, roles, permisos y datos base (Presupuesto Global)'
    password_default = 'TheStrokes94.'
    
    def handle(self, *args, **kwargs):
        self.stdout.write("🛠️ Iniciando configuración de la Municipalidad de Puyehue...")

        
        # ELIMINAMOS TODOS LOS DATOS PARA EMPEZAR FRESCO Y EVITAR CLAVES DUPLICADAS
        ActividadProyecto.objects.all().delete()
        CuentaPresupuestaria.objects.all().delete()
        Proyecto.objects.all().delete() 
        User.objects.filter(is_superuser=False).delete() # Eliminamos usuarios de prueba

        
        ct_actividad = ContentType.objects.get_for_model(ActividadProyecto)
        ct_presupuesto = ContentType.objects.get_for_model(CuentaPresupuestaria)


        grupo_admin, _ = Group.objects.get_or_create(name='Administracion_Municipal')
        grupo_daf, _ = Group.objects.get_or_create(name='Finanzas_DAF')
        grupo_lectura, _ = Group.objects.get_or_create(name='Directores_Lectura')

        permisos_admin = Permission.objects.filter(
            content_type=ct_actividad, 
            codename__in=['add_actividadproyecto', 'change_actividadproyecto', 'delete_actividadproyecto']
        )
        permiso_daf_presupuesto_change = Permission.objects.get(
            content_type=ct_presupuesto, codename='change_cuentapresupuestaria'
        )
        permiso_ver_todo = Permission.objects.filter(codename__startswith='view_')
        
        grupo_admin.permissions.set(permisos_admin)
        grupo_daf.permissions.add(permiso_daf_presupuesto_change)
        grupo_lectura.permissions.set(permiso_ver_todo)

        
        users_data = [
            {'user': 'administrador_municipal', 'email': 'admin@puyehue.cl', 'group': grupo_admin},
            {'user': 'director_finanzas', 'email': 'daf@puyehue.cl', 'group': grupo_daf},
            {'user': 'dideco', 'email': 'dideco@puyehue.cl', 'group': grupo_lectura},
            {'user': 'director_control', 'email': 'control@puyehue.cl', 'group': grupo_lectura},
            {'user': 'alcalde', 'email': 'alcalde@puyehue.cl', 'group': grupo_lectura},
        ]
        
        user_objects = {}

        for u in users_data:
            user, created = User.objects.get_or_create(username=u['user'], email=u['email'])
            user.set_password(self.password_default)
            user.is_staff = True
            user.save()
            user.groups.set([u['group']])
            user_objects[u['user']] = user 
            self.stdout.write(f"👤 Usuario {u['user']} ({u['group'].name}) -> Creado/Actualizado")

        
        CuentaPresupuestaria.objects.create(
            codigo_cuenta='000000',
            nombre_cuenta='PRESUPUESTO GENERAL ANUAL',
            presupuesto_inicial=Decimal('2500000000'),
            modificaciones=Decimal('-150000000'),
            presupuesto_vigente=Decimal('2350000000')
        )
        self.stdout.write(self.style.SUCCESS("💰 Cuenta de Presupuesto Global CREADA."))

        
        proyecto_infra, created = Proyecto.objects.get_or_create(
            codigo='PR-2025-INFRA',
            defaults={
                'nombre': 'Mejoramiento Infraestructura Comunal',
                'director_asignado': user_objects['administrador_municipal']
            }
        )
        self.stdout.write(f"🏗️ Creado Proyecto Padre: {proyecto_infra.nombre}")

        
        actividades = [
            
            {"id": "ACT-001", "nombre": "Mejoramiento Costanera Entre Lagos", "inicio": date(2025, 1, 15), "fin": date(2025, 6, 30), "estado": "En Progreso", "responsable_user": user_objects['administrador_municipal']},
            {"id": "ACT-002", "nombre": "Operativo Veterinario Rural Pilmaiquén", "inicio": date(2025, 2, 1), "fin": date(2025, 2, 5), "estado": "Pendiente", "responsable_user": user_objects['dideco']},
            {"id": "ACT-003", "nombre": "Recambio Luminarias Villa Entre Lagos", "inicio": date(2024, 11, 1), "fin": date(2024, 12, 15), "estado": "Atrasado", "responsable_user": user_objects['director_control']},
        ]

        for item in actividades:
            ActividadProyecto.objects.get_or_create(
                activity_id=item["id"],
                defaults={

                    "proyecto_padre": proyecto_infra, 
                    "responsable": item["responsable_user"], 
                    "nombre_actividad": item["nombre"],
                    "fecha_inicio": item["inicio"],
                    "fecha_termino": item["fin"],
                    "estado": item["estado"],
                    "creado_por": user_objects['administrador_municipal']
                }
            )
        self.stdout.write(self.style.SUCCESS(f"✅ Carga completa. {len(actividades)} actividades cargadas y asignadas a '{proyecto_infra.nombre}'."))

        self.stdout.write("\n🚀 EL SISTEMA ESTÁ LISTO PARA SER PROBADO.")