from django.urls import path

from .views import (
    index,
    TaskListView,
    WorkerListView,
    TaskTypeListView,
    PositionListView,
)

urlpatterns = [
    path("",index, name="index"),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    )
]

app_name = "catalog"