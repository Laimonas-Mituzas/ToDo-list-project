from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('todolist/<int:pk>', views.TodolistDetailView.as_view(), name='todolist'),
    # path('todolist/<int:owner>', views.todolist, name='todolist')
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
 ]