from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, Worker, TaskType, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed"
    )
    list_filter = (
        "task_type",
        "priority",
        "is_completed"
    )
    search_fields = (
        "name",
        "task_type__name",
        "description"
    )
    date_hierarchy = "deadline"


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "position",
        "phone_number",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "position",
                    "phone_number",
                )
            }
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                    "phone_number",
                )
            },
        ),
    )


admin.site.register(Position)
admin.site.register(TaskType)
