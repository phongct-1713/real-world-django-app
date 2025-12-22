from django.shortcuts import render
from .forms import userLoginForm, UserRegistrationForm
from django.http import HttpResponse

# Create your views here.

def login(request):
    form = userLoginForm()

    if request.method == 'POST':
        form = userLoginForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Login Successful")

    return render(request, 'login.html', {'form': form})

def register(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Registration Successful")

    return render(request, 'register.html', {'form': form})