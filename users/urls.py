from django.urls import path
from users.views import RegisterView, LoginView
from .views import AdminLoginView , AdminRegisterView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
     path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
      path('admin-register/', AdminRegisterView.as_view(), name='admin-register'),
]
