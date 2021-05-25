from django.shortcuts import render
from . import models
from django.utils import timezone


def home(request):
    task_list_load_on_home = models.Task.objects.all()
    context = {
        'task_list_load_on_home': task_list_load_on_home
    }
    return render(request, 'base.html', context)


def task(request):
    task = request.POST.get('task')
    models.Task.objects.create(task_text=task, task_time_added=timezone.now())
    task_list = models.Task.objects.all()
    context = {
        'task_list': task_list,
    }
    return render(request, 'newtask.html', context)
