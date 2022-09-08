from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


class TaskList(LoginRequiredMixin,ListView):
    context_object_name = 'tasks'
    template_name = 'todo/tasks_list.html'

    def get_queryset(self):
        return Task.objects.filter(
            user = self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] =  self.request.GET.get('search','').lstrip().replace('ㅤ',' ')
        context['tasks'] = context['tasks'].filter(title__icontains = context['search_input'])
        context['search_input'] =  context['search_input'].replace(' ','ㅤ')
        context['completed_tasks'] = context['tasks'].filter(complete_status=True)
        context['incompleted_tasks'] = context['tasks'].filter(complete_status=False)
        context['count_incompleted'] = context['incompleted_tasks'].count()
        context['count_completed'] = context['completed_tasks'].count()
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    context_object_name = 'task'
    template_name = 'todo/task.html'

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)


class TaskMarkComplete(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if (Task.objects.filter(pk = kwargs['pk']).exists()):
            task = Task.objects.get(pk = kwargs['pk'])
            task.complete_status = True
            task.save()
        return reverse_lazy('tasks')


class TaskMarkIncomplete(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if (Task.objects.filter(pk = kwargs['pk']).exists()):
            task = Task.objects.get(pk = kwargs['pk'])
            task.complete_status = False
            task.save()
        return reverse_lazy('tasks')


class TaskCreate(LoginRequiredMixin,CreateView):
    fields = ['title','description','complete_status']
    success_url = reverse_lazy('tasks')
    template_name = 'todo/task_form.html'

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_task'] = True
        return context


class TaskUpdate(LoginRequiredMixin,UpdateView):
    fields = ['title','description','complete_status']
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDelete(LoginRequiredMixin,DeleteView):
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)