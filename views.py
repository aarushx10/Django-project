from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import SignUpForm, TaskForm
from .models import Task


class OwnerQuerysetMixin(LoginRequiredMixin):
    """Users can only ever see and touch their own tasks."""

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskListView(OwnerQuerysetMixin, ListView):
    model = Task
    paginate_by = 8
    context_object_name = "tasks"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        if q:
            qs = qs.filter(title__icontains=q)
        if status in Task.Status.values:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["status"] = self.request.GET.get("status", "")
        ctx["statuses"] = Task.Status.choices
        return ctx


class TaskDetailView(OwnerQuerysetMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_message = "Task created."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(OwnerQuerysetMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_message = "Task updated."


class TaskDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        messages.success(self.request, "Task deleted.")
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
