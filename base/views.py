from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.


class CustomLoginView(LoginView):
       template_name = 'base/login.html'
       fields = '__all__'
       redirect_authenticated_user = True

       def form_valid(self, form):
        messages.success(self.request, "You have logged in successfully!")
        return super().form_valid(form)
       
       def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)
       

       def get_success_url(self):
              return reverse_lazy('tasks')
       
class RegisterPage(FormView):
      template_name = 'base/register.html' 
      form_class = UserCreationForm
      redirect_authenticated_user = True
      success_url = reverse_lazy('tasks') 
       
      def form_valid(self, form):
          user = form.save()
          if user is not None:
              login(self.request, user) 
              messages.success(self.request, "You have registered successfully!") 
                
          return super(RegisterPage, self).form_valid(form)
      
      def form_invalid(self, form):
        # Add an error message when the form fails validation
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
      
      def get(self, *args, **kwargs):
          if self.request.user.is_authenticated:
                return redirect('tasks')
          return super(RegisterPage, self).get(*args, **kwargs)  
        

class Tasklist(LoginRequiredMixin, ListView):
      model = Task
      context_object_name = 'tasks'

      def get_context_data(self, **kwargs):
      
            context = super().get_context_data(**kwargs)
            context['tasks'] = context['tasks'].filter(user=self.request.user)
            context['count'] = context['tasks'].filter(complete=False).count()

            search_input = self.request.GET.get('search-area') or ''
            if search_input:
               context['tasks'] = context['tasks'].filter(title__startswith=search_input)   
            context['search_input'] = search_input    
            return context
              


class TaskDetail(LoginRequiredMixin, DetailView):
      model = Task
      context_object_name = 'task'
      template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView): 
      model = Task
      fields = ['title', 'description', 'complete']
      success_url = reverse_lazy('tasks') 

      def form_valid(self, form):
          form.instance.user = self.request.user
          messages.success(self.request, " Item created successfully!") 
          return super(TaskCreate, self).form_valid(form)
      
        

class TaskUpdate(SuccessMessageMixin,LoginRequiredMixin, UpdateView):      
       model = Task
       fields = ['title', 'description', 'complete']
       success_url = reverse_lazy('tasks') 
       success_message = "Task updated successfully!"  
      
class DeleteView(SuccessMessageMixin,LoginRequiredMixin, DeleteView): 
            model = Task 
            queryset = Task.objects.all()
            template_name = 'base/task_confirm_delete.html'
            context_object_name = 'task'
            success_url = reverse_lazy('tasks') 
            success_message = "Task deleted successfully!"