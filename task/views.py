from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def home(request):
    return render(request, 'task/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'task/signupuser.html', {'form': UserCreationForm()})
    elif request.method == 'POST':
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttasks')
            except IntegrityError:
                return render(request, 'task/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username.'})
        else:
            # Tell the user the passwords didn't match
            return render(request, 'task/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'task/loginuser.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'task/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttasks')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttasks(request):
    return render(request, 'task/currenttasks.html')
