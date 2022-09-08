from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect


class LoginView(BaseLoginView):
    fields = '__all__'
    redirect_authenticated_user = True
    template_name = 'user/login.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')


class RegisterView(FormView):
    form_class = UserCreationForm
    redirect_authenticated_user = True
    template_name = 'user/register.html'

    def get_success_url(self) -> str:
        return reverse_lazy('tasks')
    
    def form_valid(self, form):
        user  = form.save()
        if user is not None:
            login(self.request,user)
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)