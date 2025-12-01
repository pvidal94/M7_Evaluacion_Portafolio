from django import forms
from .models import ActividadProyecto, CuentaPresupuestaria, Proyecto # AGREGAMOS PROYECTO

class ActividadForm(forms.ModelForm):
   
    class Meta:
        model = ActividadProyecto
       
        fields = ['proyecto_padre', 'activity_id', 'nombre_actividad', 'fecha_inicio', 'fecha_termino', 'estado', 'responsable']
        widgets = {
            'proyecto_padre': forms.Select(attrs={'class': 'form-select'}), 
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'activity_id': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_actividad': forms.TextInput(attrs={'class': 'form-control'}),
           
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = CuentaPresupuestaria
        fields = '__all__'
        widgets = {
            'codigo_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'presupuesto_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'modificaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'presupuesto_vigente': forms.NumberInput(attrs={'class': 'form-control'}),
        }