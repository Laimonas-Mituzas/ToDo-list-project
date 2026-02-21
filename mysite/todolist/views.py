from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Todolist, TodolistItem

def index(request):
    todo_list_counts = Todolist.objects.all().count()

    context = {'todo_list_counts': todo_list_counts}

    return render(request, template_name="index.html", context=context)


def dashboard(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
             'num_visits': num_visits,
    }
    return render(request, template_name="dashboard.html", context=context)
