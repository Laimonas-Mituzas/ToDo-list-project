from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('todolist/<int:pk>', views.TodolistDetailView.as_view(), name='todolist'),
    path("todolist/create", views.TodolistCreateView.as_view(), name="todolist_create"),
    path("todolist/<int:pk>/update", views.TodolistUpdateView.as_view(), name="todolist_update"),
    path("todolist/<int:pk>/delete", views.TodolistDeleteView.as_view(), name="todolist_delete"),
    path('todolist/<int:todolist_pk>/item/create', views.TodolistItemCreateView, name='todolist_item_create'),
    # path('todolist/<int:todolist_pk>/item/<int:item_pk>/toggle', views.TodolistItemToggleView, name='todolist_item_toggle'),
    path('todolist/<int:todolist_pk>/item/<int:item_pk>/update', views.TodolistItemUpdateView, name='todolist_item_edit'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

 ]