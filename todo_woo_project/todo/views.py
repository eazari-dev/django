from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todo/base.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        #create user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError:
                    return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Username has been taken already!'})
        else:
            #didnt mathed passwords
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password did not math!'})

def currenttodos(request):
    return render(request, 'todo/base.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did\'nt matched!'})
        else:
            login(request, user)
            return redirect('home')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')
