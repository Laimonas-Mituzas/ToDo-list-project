from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.avatar.path)

# Sarasu modelis
class Todolist(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), max_length=2000, null=True, blank=True)
    completed = models.BooleanField(verbose_name=_("Completed"), default=False)
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
    todolist = models.ForeignKey(Todolist, verbose_name=_("Todo list"), on_delete=models.CASCADE, related_name='items')
    title = models.CharField(verbose_name=_("Task"), max_length=200)
    completed = models.BooleanField(verbose_name=_("Completed"),default=False)

    class Meta:
        verbose_name = _("ToDo item")
        verbose_name_plural = _("ToDo items")

    def __str__(self):
        return self.title


