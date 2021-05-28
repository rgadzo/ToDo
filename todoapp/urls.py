from django.urls import path
from . import views

app_name = "todoapp"
urlpatterns = [
    path('', views.home, name='home'),
    path('new-task', views.task, name='task'),
    path('delete/<int:task_id>', views.delete, name='delete'),
    path('rewrite/<int:task_id>', views.rewrite, name='rewrite'),
    path('rewrite-done/<int:task_id>', views.rewrite_done, name='rewritedone'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
]
