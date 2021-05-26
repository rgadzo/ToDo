from django.contrib import admin
from .models import Task

admin.site.site_header = "ToDo Admin"
admin.site.site_title = "ToDo Admin"
admin.site.index_title = "Welcome to Admin panel"

admin.site.register(Task)
