from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Todolist, TodolistItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserChangeForm, CustomUserCreateForm, TodolistCreateUpdateForm, TodolistItemCreateForm


def index(request):
    todolists = Todolist.objects.filter(owner=request.user) # visi sarasai, kuriuos sukure vartotojas
    todolists_counts = Todolist.objects.all().count() # kiek is viso sarasu
    todolist_items = TodolistItem.objects.all() # kiek viso uzduočių visuose sarauose
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
        'todolists':  todolists,
        'todolists_counts': todolists_counts,
        'todolist_items': todolist_items,

    }

    return render(request, template_name="dashboard.html", context=context)


class TodolistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Todolist
    template_name = 'todolist.html'
    context_object_name = 'todolist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodolistItemCreateForm
        return context

    def get_queryset(self):
        return Todolist.objects.filter(owner=self.request.user)


class TodolistCreateView(LoginRequiredMixin, generic.CreateView):
    model = Todolist
    template_name = 'todolist_create.html'
    form_class = TodolistCreateUpdateForm
    #fields = ['title', 'description', 'deadline']
    # success_url = reverse_lazy('todolist/<int:pk>')

    def get_success_url(self):
        return reverse("todolist", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)



class TodolistDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Todolist
    template_name = 'todolist_delete.html'
    success_url = reverse_lazy('index')



class TodolistUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Todolist
    template_name = 'todolist_create.html'
    form_class = TodolistCreateUpdateForm

    def get_success_url(self):
        return reverse("todolist", kwargs={"pk": self.object.id})


def TodolistItemCreateView(request, todolist_pk):
    if request.method == 'POST':
        form = TodolistItemCreateForm(request.POST)
        if form.is_valid():
            todolist = Todolist.objects.get(id=todolist_pk)
            form.instance.todolist = todolist
            form.save()
            return redirect('todolist', pk=todolist_pk)
    else:
        form = TodolistItemCreateForm()
    return render(request, 'todolist.html', {'form': form})

def TodolistItemUpdateView(request, todolist_pk, item_pk):
    try:
        item = TodolistItem.objects.select_related('todolist').get(pk=item_pk, todolist__pk=todolist_pk)
    except TodolistItem.DoesNotExist:
        return redirect('todolist', pk=todolist_pk)

    if request.method == 'POST':
        form = TodolistItemUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('todolist', pk=todolist_pk)
    else:
        form = TodolistItemCreateForm(instance=item)

    return render(request, 'todolist.html', {'form': form, 'item': item})


# from django.contrib.auth.decorators import login_required
#
# @login_required
# def TodolistItemToggleView(request, todolist_pk, item_pk):
#     """Toggle or set `completed` on a TodolistItem based on submitted form data.
#     Accepts POST only and redirects back to the todolist detail.
#     """
#     if request.method != 'POST':
#         return redirect('todolist', pk=todolist_pk)
#
#     try:
#         item = TodolistItem.objects.select_related('todolist').get(pk=item_pk, todolist__pk=todolist_pk)
#     except TodolistItem.DoesNotExist:
#         return redirect('todolist', pk=todolist_pk)
#
#     # Ensure the current user owns the todolist (safety check)
#     if item.todolist.owner != request.user:
#         return redirect('todolist', pk=todolist_pk)
#
#     # Determine checkbox field name for this item and set completed accordingly.
#     checkbox_name = f'item_done_{item.pk}'
#     # If the POST contains the checkbox field, it means checked -> True; otherwise False.
#     item.completed = checkbox_name in request.POST
#     item.save()
#
#     return redirect('todolist', pk=todolist_pk)


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")
