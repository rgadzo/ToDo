from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import CreateUserForm


from . import models


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def home(request):
    task_list_load_on_home = models.Task.objects.all()
    context = {
        'task_list_load_on_home': task_list_load_on_home
    }
    return render(request, 'base.html', context)


def task(request):
    task = request.POST.get('task')
    models.Task.objects.create(task_text=task, task_time_added=timezone.now())
    return HttpResponseRedirect(reverse('todoapp:home'))


def delete(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('todoapp:home'))


def rewrite(request, task_id):
    tasks_list = models.Task.objects.all()
    return render(request, 'rewrite.html', context={
        'task_id': task_id,
        'tasks_list': tasks_list,
    })


def rewrite_done(request, task_id):
    new_task_text = request.POST.get('new-name')
    task = get_object_or_404(models.Task, id=task_id)
    task.task_text = new_task_text
    task.save()
    return HttpResponseRedirect(reverse('todoapp:home'))
