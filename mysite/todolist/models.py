from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="profile_pics", null=True, blank=True)

# Sarasu modelis
class Todolist(models.Model):
    title = models.CharField(verbose_name=_("Title"),max_length=200)
    description = models.TextField(max_length=2000, null=True, blank=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(to="todolist.CustomUser",
                              verbose_name=_("Owner"),
                              on_delete=models.SET_NULL,
                              null=True, blank=True)
    created_at = models.DateField(verbose_name=_("Created"), default=timezone.now)
    deadline = models.DateField(verbose_name=_("Deadline"), null=True, blank=True )

    class Meta:
        verbose_name = _("ToDo list"),
        verbose_name_plural = _("ToDo lists")

    def total_items(self):
        return self.items.count()

    def is_completed(self):
        return self.items.count() > 0 and self.items.filter(completed=False).count() == 0

    def is_overpassed(self):
        return self.deadline and timezone.now().date() > self.deadline


    def __str__(self):
        return self.title

# Uzduociu modelis
class TodolistItem(models.Model):
    todolist = models.ForeignKey(Todolist, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(verbose_name=_("Task"), max_length=200)
    completed = models.BooleanField(verbose_name=_("Completed"),default=False)

    class Meta:
        verbose_name = _("ToDo item")
        verbose_name_plural = _("ToDo items")

    def __str__(self):
        return self.title


