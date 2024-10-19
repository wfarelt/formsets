# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Task
from .forms import CategoryForm, TaskForm
from django.forms import modelformset_factory

# CRUD de Category
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')

# Vista para añadir múltiples tasks a una categoría

def add_tasks_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Creamos un formset con las tareas de la categoría
    TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1, can_delete=True)
    if request.method == 'POST':
        formset = TaskFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                task = form.save(commit=False)
                task.category = category
                task.save()
        else:
            for form in formset[:-1]:
                task = form.save(commit=False)
                task.category = category
                task.save()
            # Eliminar tareas marcadas para eliminación
            for form in formset.forms:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.pk:  # Asegurarse de que la tarea exista en la BD
                        form.instance.delete()
            # Redirigimos a add_tasks para añadir más tareas
        return redirect('add_tasks_to_category', category_id=category_id)
    else:
        formset = TaskFormSet(queryset=Task.objects.all().filter(category=category))
    return render(request, 'add_tasks.html', {'formset': formset, 'category': category})
