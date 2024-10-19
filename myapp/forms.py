# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Category, Task
import datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'due_date', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre de la tarea'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
 

# Formset para gestionar varias tareas a la vez
TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1, can_delete=True)
