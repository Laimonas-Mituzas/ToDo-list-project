from django.contrib import admin
from .models import Todolist, TodolistItem
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('avatar',)}),
    )

class TodolistAdminInline(admin.TabularInline):
    model = TodolistItem
    extra = 0
    can_delete = False
    fields = ['title', 'completed']

class TodolistAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'total_items', 'deadline', 'created_at' ]
    list_filter = ['owner']
    search_fields = ['items__title']  #  search by item title
    inlines = [TodolistAdminInline]


class TodolistItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'todolist', 'completed']
    list_filter = ['todolist']
    search_fields = ['title']

# Register your models here.
admin.site.register(Todolist, TodolistAdmin)
admin.site.register(TodolistItem, TodolistItemAdmin)
admin.site.register(CustomUser, CustomUserAdmin)