from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('todolist/<int:pk>', views.TodolistDetailView.as_view(), name='todolist'),
    path("todolist/create", views.TodolistCreateView.as_view(), name="todolist_create"),
    path("todolist/<int:pk>/update", views.TodolistUpdateView.as_view(), name="todolist_update"),
    path("todolist/<int:pk>/delete", views.TodolistDeleteView.as_view(), name="todolist_delete"),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

 ]