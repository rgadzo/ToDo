from django.db.models.fields import EmailField
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


from . import models


def check_does_email_already_exist(mail):
    all_emails = models.User.objects.values_list('email', flat=True)
    valid = False
    for email in all_emails:
        if email != mail:
            valid = True
        else:
            valid = False
    return valid


@login_required(login_url='todoapp:login')
def logoutPage(request):
    logout(request)
    return redirect('todoapp:login')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('todoapp:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('uname')
            password = request.POST.get('passwd')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todoapp:home')
            else:
                messages.warning(
                    request, "Your password or username isn't valid")
                return redirect('todoapp:login')
        else:
            pass

        return render(request, 'login.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('todoapp:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            email = request.POST.get('email')
            if form.is_valid():
                if check_does_email_already_exist(email):
                    form.save()
                    messages.success(request, "User is registered sucessfully")
                    return redirect('todoapp:login')
                else:
                    messages.warning(
                        request, "User with same email already exist")
            else:
                messages.warning(
                    request, "That username already exist or your password is too short")
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)


@login_required(login_url='todoapp:login')
def home(request):
    current_user = request.user
    user_model = models.User.objects.get(id=current_user.id)
    task_list_load_on_home = user_model.task_set.all()
    context = {
        'task_list_load_on_home': task_list_load_on_home
    }
    return render(request, 'base.html', context)


@login_required(login_url='todoapp:login')
def task(request):
    task = request.POST.get('task')
    current_user = request.user
    user_model = models.User.objects.get(id=current_user.id)
    user_model.task_set.create(task_text=task, task_time_added=timezone.now())
    return HttpResponseRedirect(reverse('todoapp:home'))


@login_required(login_url='todoapp:login')
def delete(request, task_id):
    current_user = request.user
    user_model = models.User.objects.get(id=current_user.id)
    task = get_object_or_404(user_model.task_set, id=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('todoapp:home'))


@login_required(login_url='todoapp:login')
def rewrite(request, task_id):
    current_user = request.user
    user_model = models.User.objects.get(id=current_user.id)
    tasks_list = user_model.task_set.all()
    return render(request, 'rewrite.html', context={
        'task_id': task_id,
        'tasks_list': tasks_list,
    })


@login_required(login_url='todoapp:login')
def rewrite_done(request, task_id):
    new_task_text = request.POST.get('new-name')
    current_user = request.user
    user_model = models.User.objects.get(id=current_user.id)
    task = get_object_or_404(user_model.task_set, id=task_id)
    task.task_text = new_task_text
    task.save()
    return HttpResponseRedirect(reverse('todoapp:home'))
