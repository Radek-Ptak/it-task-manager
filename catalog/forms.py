from django.utils import timezone

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, MinLengthValidator
from django.urls import reverse_lazy
from django.utils.html import format_html

from catalog.models import Task, Worker


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(
                3,
                message=(
                    "Task name must contain at least 3 characters."
                )
            )
        ]
    )
    description = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(
                10,
                message=(
                    "Description must contain at least 10 characters."
                )
            )
        ]
    )
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
    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if (
            deadline < timezone.localdate() and not self.instance.pk
        ):
            raise forms.ValidationError(
                "Deadline cannot be in the past."
            )
        return deadline

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
    phone_number = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                r"^\+?[0-9 ]{9,15}$",
                message=(
                    "Phone number must contain 9–15 digits "
                    "and may start with '+'."
                )
            )
        ]
    )


    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                r"^\+?[0-9 ]{9,15}$",
                message=(
                    "Phone number must contain 9–15 digits "
                    "and may start with '+'."
                )
            )
        ]
    )

    class Meta:
        model = Worker
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "position",
        )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is None or not user.is_staff:
            self.fields.pop("position", None)
