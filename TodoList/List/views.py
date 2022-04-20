from pyexpat import model
from re import template
from attr import fields
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView,CreateView,UpdateView, DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name="List/login.html"
    fields = '__all__'
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPageView(FormView):
    template_name= "List/register.html"
    form_class= UserCreationForm
    redirect_authenticated_user= True
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user )
        return super(RegisterPageView,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPageView, self).get(*args,**kwargs)



class TaskView(LoginRequiredMixin,ListView):
    model =Task
    context_object_name= 'tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']= context['tasks'].filter(
                title__icontains=search_input
            )
        return context

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task

class TaskCreateView(LoginRequiredMixin,CreateView):
    model =Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreateView, self).form_valid(form)

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model=Task
    fields= '__all__'
    success_url= reverse_lazy('tasks')

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model= Task
    context_object_name= 'task'
    success_url= reverse_lazy('tasks')


