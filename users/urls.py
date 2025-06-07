# urls.py
from rest_framework.authtoken.views import obtain_auth_token
from .views import AdminLoginView
from django.urls import path
urlpatterns = [
  
   path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),
]
