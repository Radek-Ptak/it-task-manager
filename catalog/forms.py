from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.html import format_html

from catalog.models import Task, Worker


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees",
        )
        widgets = {
            "deadline": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe the task...",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter task name...",
                }
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task_type"].help_text = format_html(
            'Don’t see the right type? '
            '<a href="{}">Create a new task type</a>.',
            reverse_lazy("catalog:task-type-create"),
        )
        if user is None or not user.is_staff:
            self.fields.pop("assignees", None)


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "position",
        )
