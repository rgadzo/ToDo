from django.db import models
from django.db.models.fields import DateField


class Task(models.Model):
    task_text = models.CharField(max_length=200)
    task_time_added = models.DateField('date time')

    def __str__(self):
        return self.task_text
