from django.urls import path
from .views import home, register, CustomLoginView
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]  
