from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Todolist(models.Model):
    title = models.CharField(verbose_name="Title",max_length=200)
    description = models.TextField(max_length=2000, null=True, blank=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User,
                              verbose_name="Savininkas",
                              on_delete=models.SET_NULL,
                              null=True, blank=True)
    created_at = models.DateField(verbose_name="Created", default=timezone.now)
    deadline = models.DateField(verbose_name="Deadline", null=True, blank=True )

    class Meta:
        verbose_name = 'ToDo list'
        verbose_name_plural = 'ToDo lists'

    def total_items(self):
        return self.items.count()

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back


    def __str__(self):
        return self.title

class TodolistItem(models.Model):
    todolist = models.ForeignKey(Todolist, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(verbose_name="Title", max_length=200)
    # description = models.TextField(max_length=2000,null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ToDo item'
        verbose_name_plural = 'ToDo items'

    def __str__(self):
        return self.title

