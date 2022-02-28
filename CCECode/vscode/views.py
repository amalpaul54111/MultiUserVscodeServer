from email.mime import base
from multiprocessing import context
from re import T, sub
from telnetlib import DO
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from .models import Docker
import subprocess

# Create your views here.
def register_request(request):
    context ={}
    if(request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            subprocess.check_output(f"cd ../Files && mkdir {username}", shell=True)
            return redirect('/')
        if(request.POST['password1'] != request.POST['password2']):
            context["error"] = "Retype the same password"
            return render (request=request, template_name="index.html",context=context)
    return render (request=request, template_name="index.html",context=context)
    


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                print(Docker.objects.get(user=user))
                return redirect('/')
            except:
                port = Docker.objects.filter(used=False).first()
                print(port)
                port.used = True;
                port.user = user
                print("Logged In")
                output = subprocess.check_output(f'cd ../Files/{username} && docker run -it --init -dp {port.port}:3000 -v "$(pwd):/home/workspace:cached" code', shell=True)
                print(output)
                port.container = output
                port.save()
                return redirect('/')
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "index.html", context)
    else:
	    return render (request=request, template_name="index.html",context=context)

def user_logout(request):
    docker = Docker.objects.get(user=request.user)
    docker.used = False
    docker.user = None
    output = subprocess.check_output(f'docker stop {docker.container}')
    docker.save()
    logout(request)
    return redirect('/login')


@login_required(login_url="/login")
def homepage(request):
    base_url = "http://localhost:"
    port = Docker.objects.get(user = request.user)
    url = base_url + port.port
    return render(request=request, template_name="vscode.html", context={"url":url})