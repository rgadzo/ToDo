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
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.urls import reverse
from datetime import date, datetime
import string
import random
from django.conf import settings


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


def resend(request, resend_id):
    ssrid = request.session['resend_id']
    confirm_id = request.session['confirm_id']
    if str(ssrid) == str(resend_id):
        confirmation_number = request.session['confirmation_code']
        uname = request.session['username']
        email = request.session['email']
        mail_content_template = render_to_string('email_template.html', {
            'confirmation_number': confirmation_number,
            'name': uname,
        })
        try:
            send_mail(
                'Confirmation',
                mail_content_template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except BadHeaderError:
            print('Bad header configuration, preventing header injection')
        return redirect('todoapp:confirm', confirm_id=confirm_id)
    else:
        return redirect('todoapp:confirm', confirm_id=confirm_id)


def confirm(request):
    sscid = request.session['sscid']
    if str(sscid):
        if request.user.is_authenticated:
            return redirect('todoapp:home')
        else:
            resend_id = random.randint(1000000, 3000000)
            request.session['resend_id'] = resend_id
            mail_host = request.session['mail_host']
            if request.method == 'POST':
                code = request.session['confirmation_code']
                user_username = request.session['username']
                user_password = request.session['password']
                user_mail = request.session['email']
                entered_code = request.POST.get('code')
                if str(code) == str(entered_code):
                    user = models.User.objects.create(
                        username=user_username, email=user_mail)
                    user.set_password(user_password)
                    user.save()
                    messages.success(
                        request, "User is registered successfully")
                    return redirect('todoapp:login')
                else:
                    messages.warning(request, "Confirmation code is incorrect")
                    return redirect('todoapp:confirm')

            else:
                pass

            context = {
                'mail_host': mail_host,
                'resend_id': resend_id,
            }
            return render(request, 'verfication.html', context)
    else:
        redirect('todoapp:register')


@login_required(login_url='todoapp:login')
def logoutPage(request):
    logout(request)
    return redirect('todoapp:login')


@login_required(login_url='todoapp:login')
def resetPassword(request):
    passwd1 = request.POST.get('passwd1')
    passwd2 = request.POST.get('passwd2')
    if request.method == 'POST':
        if passwd1 == passwd2:
            user_model = models.User.objects.get(id=request.user.id)
            user_model.set_password(passwd1)
            user_model.save()
            logout(request)
            messages.success(request, "Password changed successfully")
            return redirect('todoapp:login')
        else:
            messages.warning(request, "Two passwords do not match")
            return redirect('todoapp:passwdreset')
    else:
        pass

    return render(request, 'reset.html')


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
            uname = request.POST.get('username')
            passwd = request.POST.get('password1')
            if form.is_valid():
                if check_does_email_already_exist(email):
                    mail_host = email.split('@')[1].split('.')[0]
                    confirmation_number = random.randint(100000, 2000000)
                    request.session['confirmation_code'] = confirmation_number
                    request.session['username'] = uname
                    request.session['password'] = passwd
                    request.session['email'] = email
                    request.session['mail_host'] = mail_host
                    mail_content_template = render_to_string('email_template.html', {
                        'confirmation_number': confirmation_number,
                        'name': uname,
                    })
                    try:
                        send_mail(
                            'Confirmation',
                            mail_content_template,
                            settings.EMAIL_HOST_USER,
                            [email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        print('Bad header configuration, preventing header injection')
                    sscid = random.randint(1000000, 3000000)
                    request.session['sscid'] = sscid
                    return redirect('todoapp:confirm')
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

    current_date = date.today().strftime("%B %d")

    task_list_load_on_home = user_model.task_set.all()
    context = {
        'task_list_load_on_home': task_list_load_on_home,
        'current_date': current_date,
    }
    return render(request, 'base.html', context)


@login_required(login_url='todoapp:login')
def task(request):
    alphabet_str = string.ascii_lowercase + string.ascii_uppercase
    alphabet_list = list(alphabet_str)

    task = request.POST.get('task')

    task_is_valid = True

    for letter in alphabet_list:
        if letter in task:
            task_is_valid = True
            break
        else:
            task_is_valid = False

    if task_is_valid == False:
        messages.warning(request, "You can't add empty task")
        return redirect('todoapp:home')
    else:
        current_user = request.user
        user_model = models.User.objects.get(id=current_user.id)
        user_model.task_set.create(
            task_text=task, task_time_added=timezone.now())
        return redirect('todoapp:home')


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
