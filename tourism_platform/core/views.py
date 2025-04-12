from django.shortcuts import render, redirect  
from django.contrib.auth import login  
from .forms import RegistrationForm  
from django.contrib.auth.views import LoginView  

class CustomLoginView(LoginView):  
    template_name = 'core/login.html'  
    redirect_authenticated_user = True  # Перенаправлять авторизованных пользователей  

def home(request):
    return render(request, 'core/home.html')

def register(request):  
    if request.method == 'POST':  
        form = RegistrationForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            login(request, user)  
            return redirect('core/home.html')  # Замените 'home' на имя вашего URL
    else:  
        form = RegistrationForm()  
    return render(request, 'core/register.html', {'form': form})  
# Create your views here.
