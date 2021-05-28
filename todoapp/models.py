from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    task_text = models.CharField(max_length=200)
    task_time_added = models.DateField('date time')

    def __str__(self):
        return self.task_text
