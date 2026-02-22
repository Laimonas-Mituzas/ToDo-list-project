from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Todolist, TodolistItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    todo_list_counts = Todolist.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
        'todo_list_counts': todo_list_counts,
        'todolists':  Todolist.objects.all(),
    }

    return render(request, template_name="dashboard.html", context=context)


# def dashboard(request):
#     todolists = Todolist.objects.all()
#     context = {
#              todolists: todolists,
#     }
#     return render(request, template_name="dashboard.html", context=context)

# class TodolistView(LoginRequiredMixin, generic.ListView):
#     model = Todolist
#     template_name = 'dashboard.html'
#     context_object_name = 'todolists'
#
#     def get_queryset(self):
#         return Todolist.objects.filter(owner=self.request.user)  # type: ignore[attr-defined]

class todolist_create(LoginRequiredMixin, generic.CreateView):
    model = Todolist
    template_name = 'todolist_form.html'
    fields = ['title', 'description', 'deadline']

    def form_valid(self, form):
        form.instance.owner = self.request.user  # type: ignore[attr-defined]
        return super().form_valid(form)

class todo_create(LoginRequiredMixin, generic.CreateView):
    # model = TodolistItem
    # template_name = 'todo_form.html'
    # fields = ['todolist', 'title', 'description']
    pass

