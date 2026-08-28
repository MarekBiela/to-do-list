from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Task, Tag
from .forms import TaskForm


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.prefetch_related("tags")


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("things_to_do_list:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("things_to_do_list:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("things_to_do_list:index")


class TagListView(generic.ListView):
    model = Tag


class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("things_to_do_list:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("things_to_do_list:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("things_to_do_list:tag-list")


def toggle_complete_undo_task(request, pk):
    task = Task.objects.get(id=pk)
    task.is_done = not task.is_done
    task.save()
    return HttpResponseRedirect(reverse_lazy("things_to_do_list:index"))
