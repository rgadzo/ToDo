from django.urls import path
from . import views

app_name = "todoapp"
urlpatterns = [
    path('new-task', views.task, name='task'),
    path('', views.home, name='home'),
]
