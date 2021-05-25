from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


def task(request):
    return render(request, 'newtask.html')
