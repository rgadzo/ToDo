from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse


from . import models


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
    models.Task.objects.filter(id=task_id).delete()
    return HttpResponseRedirect(reverse('todoapp:home'))


def rewrite(request, task_id):
    task = models.Task.objects.get(id=task_id)
    return render(request, 'rewrite.html', context={
        'task': task,
    })


def rewrite_done(request, task_id):
    new_task_text = request.POST.get('new-name')
    task = models.Task.objects.get(id=task_id)
    task.task_text = new_task_text
    task.save()
    return HttpResponseRedirect(reverse('todoapp:home'))
