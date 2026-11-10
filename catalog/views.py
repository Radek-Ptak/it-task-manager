from django.shortcuts import render

from catalog.models import Worker, Task


def index(request):
    """View function for the home page of the site."""

    num_worker = Worker.objects.count()
    num_task = Task.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_worker': num_worker,
        'num_task': num_task,
        'num_visits': num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)
