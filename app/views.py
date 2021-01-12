from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .decorators import unauthenticated_user
from .forms import  CreateUserForm

@login_required(login_url = 'login')
def index(request):
    return render(request, 'app/index.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'app/login.html')

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Akun berhasil dibuat' + user)
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'app/register.html', context=context)

def forgot_pass(request):
    return render(request,'app/password.html')

@login_required(login_url = 'login')
def filetable(request):
    files = File.objects.all()
    context = {'files': files}
    return render(request, 'app/filetable.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'app/upload.html', context=context)


            