from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from catalog.models import Worker, Task, TaskType, Position


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


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    )
    template_name = "catalog/task_list.html"
    context_object_name = "tasks"
    paginate_by = 5


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related(
        "assignees__position"
    )


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related(
        "position"
    )
    template_name = "catalog/worker_list.html"
    context_object_name = "workers"
    paginate_by = 5


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related(
        "position"
    ).prefetch_related(
        "tasks"
    )


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
