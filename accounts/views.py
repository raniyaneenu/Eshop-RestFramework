from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . models import *
# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['psw']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)

            print(user)
            return redirect('/')
        else:
            messages.warning(request, 'check your credentials again!!!') 
            return redirect('login')
    else:
        return render(request,'login.html')


def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
    
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already exist')
                return redirect('register')
            else:
                user=User.objects.create_user(email=email,username=username,password=password1,first_name=first_name)
                user.save() 
                return redirect('login')
                
        else:
            messages.info(request, 'passwords are not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

