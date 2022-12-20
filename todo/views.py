from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm   
from django.utils import timezone
from .models import Todo
from django.contrib.auth.decorators import login_required


def signUp(request):
   if(request.method == "GET"):
      return render(request, 'todo/signup.html', {'form': UserCreationForm()})
   else:
      if request.POST['password1'] == request.POST['password2']:
         try:
            user =  User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('currenttodos')
         except IntegrityError:
            return render(request, 'todo/signup.html', {'error': 'Пользователь с таким именем уже существует!', 'form': UserCreationForm()})
            
      else:
         return render(request, 'todo/signup.html', {'error': 'Пароли не совпадают', 'form': UserCreationForm()})
         
         

def loginuser(request):
   if(request.method == "GET"):
      return render(request, 'todo/login.html', {'form': AuthenticationForm()})
   else:
      user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
      if user is None:
         return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Имя пользователя или пароль не совпадают'})
      else:
         login(request, user)
         return redirect('currenttodos')

def currenttodos(request):
   todos = Todo.objects.filter(user = request.user, datecomplited__isnull=True)
   return render(request, 'todo/currenttodos.html', {'todos':todos})
   

def logoutuser(request):
   if request.method == 'POST':
      logout(request)
      return redirect('home')
   
def home(request):
   return render(request, 'todo/home.html')

@login_required
def createtodo(request):
   if request.method == 'GET':
      return render(request, 'todo/createtodo.html', {'form': TodoForm()})
   else:
      try:
         form = TodoForm(request.POST)
         newTodo = form.save(commit=False)
         newTodo.user = request.user
         newTodo.save()
         return redirect('currenttodos')
      except ValueError:
         return render(request, 'todo/createtodo.html', {'error': 'Неверные данные'})
         
         
@login_required        
def viewtodo(request, todo_pk):
   todo = get_object_or_404(Todo, pk=todo_pk, user=request.user )
   if request.method == 'GET':
      form = TodoForm(instance=todo)
      return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
   
   else:
      try:
         form = TodoForm(request.POST, instance=todo)
         form.save()
         return redirect('currenttodos')
      except ValueError:
         return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'errod': 'Неверные данные!!!!'})

@login_required      
def completetodo(request, todo_pk):
   todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
   if request.method == 'POST':
      todo.datecomplited = timezone.now()
      todo.save()
      return redirect('currenttodos')
      
@login_required     
def deletetodo(request, todo_pk):
   todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
   if request.method == 'POST':
      todo.delete()
      return redirect('currenttodos')
   
@login_required
def completedtodos(request):
   todos = Todo.objects.filter(user = request.user, datecomplited__isnull=False)
   return render(request, 'todo/completedtodos.html', {'todos':todos})