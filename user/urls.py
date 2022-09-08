from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, RegisterView

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',RegisterView.as_view(),name = 'register')
]