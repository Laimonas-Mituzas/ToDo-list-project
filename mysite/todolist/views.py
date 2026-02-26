from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Todolist, TodolistItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserChangeForm, CustomUserCreateForm, TodolistItemCreateForm, TodolistCreateUpdateForm, TodolistItemCreateUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q


def index(request):
    if request.user.is_authenticated:
        todolists = Todolist.objects.filter(owner=request.user)
    else:
        todolists = Todolist.objects.none()
    todolists_counts = Todolist.objects.all().count()
    todolist_items = TodolistItem.objects.all()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
        'todolists': todolists ,
        'todolists_counts': todolists_counts,
        'todolist_items': todolist_items,
    }

    # Pridedame vartotojo statistiką
    context.update(get_user_stats(request.user))

    return render(request, template_name="dashboard.html", context=context)


class TodolistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Todolist
    template_name = 'todolist.html'
    context_object_name = 'todolist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodolistItemCreateForm
        context.update(get_user_stats(self.request.user))
        return context

    def get_queryset(self):
        return Todolist.objects.filter(owner=self.request.user)


class TodolistCreateView(LoginRequiredMixin, generic.CreateView):
    model = Todolist
    template_name = 'todolist_create.html'
    form_class = TodolistCreateUpdateForm

    def get_success_url(self):
        return reverse("todolist", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_stats(self.request.user))
        return context



class TodolistDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Todolist
    template_name = 'todolist_delete.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_stats(self.request.user))
        return context



class TodolistUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Todolist
    template_name = 'todolist_create.html'
    form_class = TodolistCreateUpdateForm

    def get_success_url(self):
        return reverse("todolist", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_stats(self.request.user))
        return context


def TodolistItemCreateView(request, todolist_pk):
    if request.method == 'POST':
        form = TodolistItemCreateUpdateForm(request.POST)
        if form.is_valid():
            todolist = Todolist.objects.get(id=todolist_pk)
            form.instance.todolist = todolist
            form.save()
            return redirect('todolist', pk=todolist_pk)
    else:
        form = TodolistItemCreateUpdateForm()

    context = {'form': form}
    context.update(get_user_stats(request.user))
    return render(request, 'todolist.html', context)


@login_required
def TodolistItemEditView(request, todolist_pk, item_pk):
    try:
        item = TodolistItem.objects.select_related('todolist').get(pk=item_pk, todolist__pk=todolist_pk)
    except TodolistItem.DoesNotExist:
        return redirect('todolist', pk=todolist_pk)

    # Ensure the current user owns the todolist (safety check)
    if item.todolist.owner != request.user:
        return redirect('todolist', pk=todolist_pk)

    if request.method == 'POST':
        form = TodolistItemCreateUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('todolist', pk=todolist_pk)
    else:
        form = TodolistItemCreateUpdateForm(instance=item)

    context = {
        'form': form,
        'todolist': item.todolist,
        'item': item
    }
    context.update(get_user_stats(request.user))
    return render(request, 'todolist_item_edit.html', context)


@login_required
def TodolistItemDeleteView(request, todolist_pk, item_pk):
    """Delete a TodolistItem (POST only). Redirects back to the todolist detail."""
    try:
        item = TodolistItem.objects.select_related('todolist').get(pk=item_pk, todolist__pk=todolist_pk)
    except TodolistItem.DoesNotExist:
        return redirect('todolist', pk=todolist_pk)

    # Ensure the current user owns the todolist (safety check)
    if item.todolist.owner != request.user:
        return redirect('todolist', pk=todolist_pk)

    if request.method == 'POST':
        item.delete()
        return redirect('todolist', pk=todolist_pk)

    # If not POST, redirect back (safety)
    return redirect('todolist', pk=todolist_pk)


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_stats(self.request.user))
        return context


class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


def get_user_stats(user):
    """Grąžina vartotojo užduočių statistiką"""
    if not user.is_authenticated:
        return {}

    return {
        'todolist_items_count': TodolistItem.objects.filter(todolist__owner=user).count(),
        'todolist_items_completed': TodolistItem.objects.filter(todolist__owner=user, completed=True).count(),
        'todolist_items_not_completed': TodolistItem.objects.filter(todolist__owner=user, completed=False).count(),
        'todolists_overdue': Todolist.objects.filter(
            owner=user,
            deadline__lt=timezone.now().date(),
            completed=False
        ).count(),
        'todolist_items_overdue': TodolistItem.objects.filter(
            todolist__owner=user,
            todolist__deadline__lt=timezone.now().date(),
            completed=False
        ).count(),
    }



class OverdueItemsView(LoginRequiredMixin, generic.ListView):
    """Rodo visus praterminuotus (overdue) TodolistItem, priklausančius prisijungusiam vartotojui"""
    model = TodolistItem
    template_name = 'overdue_items.html'
    context_object_name = 'items'
    paginate_by = 25

    def get_queryset(self):
        return TodolistItem.objects.filter(
            todolist__owner=self.request.user,
            todolist__deadline__lt=timezone.now().date(),
            completed=False
        ).select_related('todolist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_stats(self.request.user))
        return context


class OverdueListsView(LoginRequiredMixin, generic.ListView):
    """Rodo visus praterminuotus Todolist (sąrašus) priklausančius prisijungusiam vartotojui"""
    model = Todolist
    template_name = 'overdue_lists.html'
    context_object_name = 'lists'
    paginate_by = 25

    def get_queryset(self):
        return Todolist.objects.filter(
            owner=self.request.user,
            deadline__lt=timezone.now().date(),
            completed=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_stats(self.request.user))
        return context
