from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import TaskForm, WorkerCreationForm
from catalog.mixins import StaffOrTaskAuthorMixin, StaffRequiredMixin, StaffOrOwnerMixin
from catalog.models import Worker, Task, TaskType, Position


@login_required
def index(request):
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    )
    template_name = "catalog/task_list.html"
    context_object_name = "tasks"
    paginate_by = 3


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related(
        "assignees__position"
    )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("catalog:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if not self.request.user.is_staff:
            self.object.assignees.add(self.request.user)
        return response


class TaskUpdateView(
    LoginRequiredMixin,
    StaffOrTaskAuthorMixin,
    generic.UpdateView
):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("catalog:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskDeleteView(
    LoginRequiredMixin,
    StaffOrTaskAuthorMixin,
    generic.DeleteView
):
    model = Task
    success_url = reverse_lazy("catalog:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related(
        "position"
    )
    template_name = "catalog/worker_list.html"
    context_object_name = "workers"
    paginate_by = 3


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related(
        "position"
    ).prefetch_related(
        "tasks"
    )


class WorkerCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.CreateView
):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("catalog:worker-list")


class WorkerUpdateView(
    LoginRequiredMixin,
    StaffOrOwnerMixin,
    generic.UpdateView
):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("catalog:worker-list")


class WorkerDeleteView(
    LoginRequiredMixin,
    StaffOrOwnerMixin,
    generic.DeleteView
):
    model = Worker
    success_url = reverse_lazy("catalog:worker-list")


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "catalog/task_type_list.html"
    context_object_name = "task_types"
    paginate_by = 5

    def get_queryset(self):
        return TaskType.objects.annotate(
            tasks_count=Count("tasks"),
        ).prefetch_related(
            "tasks",
        )


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "catalog/task_type_form.html"
    success_url = reverse_lazy("catalog:task-type-list")


class TaskTypeUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.UpdateView
):
    model = TaskType
    fields = "__all__"
    template_name = "catalog/task_type_form.html"
    success_url = reverse_lazy("catalog:task-type-list")


class TaskTypeDeleteView(
    LoginRequiredMixin,
    StaffOrTaskAuthorMixin,
    generic.DeleteView
):
    model = TaskType
    template_name = "catalog/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("catalog:task-type-list")


class PositionListView(generic.ListView):
    model = Position
    template_name = "catalog/position_list.html"
    context_object_name = "positions"
    paginate_by = 5

    def get_queryset(self):
        return Position.objects.annotate(
            workers_count=Count("workers")
        ).prefetch_related(
            "workers",
        )

class PositionCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.CreateView
):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")


class PositionUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.UpdateView
):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")


class PositionDeleteView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.DeleteView
):
    model = Position
    success_url = reverse_lazy("catalog:position-list")
