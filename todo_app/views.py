from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Task
from .forms import TaskForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('todo_app:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            get_user = User.objects.get(username=username)
        except:
            messages.error
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('todo_app:index')
        else:
            messages.error(request, "Incorrect credentials")

    context = {
        'page': page,
    }
    return render(request, 'todo_app/login_register.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('todo_app:index')

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('todo_app:index')
        else:
            messages.error(request, "Unable to register, please use different username")
    context = {
        'form': form,
    }
    return render(request, 'todo_app/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('todo_app:login')

@login_required(login_url="todo_app:login")
def index(request):
    user = request.user
    all_tasks = user.task_set.all()
    in_progress_tasks = all_tasks.filter(is_completed=False)
    completed_tasks = all_tasks.filter(is_completed=True)
    context = {
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'todo_app/index.html', context)

@login_required(login_url="todo_app:login")
def mark_complete_or_incomplete(request, pk):
    task = Task.objects.get(id=pk)
    task.is_completed = not task.is_completed
    task.save()
    messages.success(request, "Task status changed")
    return redirect('todo_app:index')
    
@login_required(login_url="todo_app:login")
def add_task(request):
    form = TaskForm()
    if request.method == 'POST':
        task = request.POST.get('task_name')
        Task.objects.create(
            task_user=request.user,
            task_name=task,
            is_completed=False,
        )
        messages.success(request, "Task Added")
        return redirect('todo_app:index')
    context = {
        'form': form
    }
    return render(request, 'todo_app/add_task.html', context)


@login_required(login_url="todo_app:login")
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method =='POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Updated")
            return redirect('todo_app:index')
    context = {
        'form': form,
    }
    return render(request, 'todo_app/add_task.html', context)


@login_required(login_url="todo_app:login")
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.info(request, "Task Deleted")
    return redirect('todo_app:index')

