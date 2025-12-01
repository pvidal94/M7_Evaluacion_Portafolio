from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count
from django.contrib import messages
from .models import ActividadProyecto, CuentaPresupuestaria
from .forms import ActividadForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Métricas Clave
    total_presupuesto = CuentaPresupuestaria.objects.aggregate(Sum('presupuesto_vigente'))['presupuesto_vigente__sum'] or 0
    actividades_pendientes = ActividadProyecto.objects.filter(estado='Pendiente').count()
    actividades_atrasadas = ActividadProyecto.objects.filter(estado='Atrasado').count()
    
    # ORM Avanzado para la Lista Caliente: Top 5 Tareas Atrasadas
    tareas_criticas = ActividadProyecto.objects.filter(
        estado='Atrasado'
    ).select_related('proyecto_padre', 'responsable').order_by('fecha_termino')[:5]
    
    context = {
        'total_presupuesto': total_presupuesto,
        'actividades_pendientes': actividades_pendientes,
        'actividades_atrasadas': actividades_atrasadas,
        'tareas_criticas': tareas_criticas,
    }
    return render(request, 'dashboard.html', context)

@login_required
def memoria_tecnica(request):
    return render(request, 'memoria_tecnica.html')

@login_required
def lista_actividades(request):
    actividades = ActividadProyecto.objects.all().order_by('fecha_inicio')
    
    resumen = {
        'total': actividades.count(),
        'atrasadas': actividades.filter(estado='Atrasado').count(),
        'en_progreso': actividades.filter(estado='En Progreso').count()
    }
    
    return render(request, 'lista_actividades.html', {
        'actividades': actividades,
        'resumen': resumen
    })

@login_required
def detalle_actividad(request, pk):
    actividad = get_object_or_404(ActividadProyecto, pk=pk)
    return render(request, 'detalle_actividad.html', {'actividad': actividad})

@login_required
@permission_required('gestion_municipal.add_actividadproyecto', raise_exception=True)
def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.creado_por = request.user
            actividad.save()
            return redirect('lista_actividades')
    else:
        form = ActividadForm()
    return render(request, 'form_actividad.html', {'form': form})

@login_required
@permission_required('gestion_municipal.change_actividadproyecto', raise_exception=True)
def editar_actividad(request, id):
    actividad = get_object_or_404(ActividadProyecto, id=id)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad actualizada correctamente.')
            return redirect('lista_actividades')
    else:
        form = ActividadForm(instance=actividad)
    return render(request, 'form_actividad.html', {'form': form, 'edit': True})

@login_required
@permission_required('gestion_municipal.delete_actividadproyecto', raise_exception=True)
def eliminar_actividad(request, id):
    actividad = get_object_or_404(ActividadProyecto, id=id)
    actividad.delete()
    messages.success(request, 'Actividad eliminada correctamente.')
    return redirect('lista_actividades')

@login_required
def reporte_gestion(request):
    reporte_atrasos = ActividadProyecto.objects.filter(
        estado='Atrasado'
    ).values('responsable').annotate(
        total_atrasos=Count('id')
    ).order_by('-total_atrasos')
    
    return render(request, 'reporte_gestion.html', {'reporte': reporte_atrasos})