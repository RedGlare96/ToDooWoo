from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from .forms import CreateForm
from .models import Todo


def home(request, view_mode=0):
    todos = []
    if request.user.is_authenticated:
        if view_mode == 0:
            todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
        elif view_mode == 1:
            todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/home.html', {'todos': todos, 'view_mode': view_mode})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('todo:home')
            except IntegrityError:
                return render(request, 'todo/signup.html',
                              {'form': UserCreationForm(), 'errormessage': 'The username is taken'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'errormessage': 'The passwords do not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),
                                                           'errormessage': 'The username and password do not match'})
        else:
            login(request, user)
            return redirect('todo:homedef')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('todo:homedef')


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': CreateForm()})
    elif request.method == 'POST':
        try:
            form = CreateForm(request.POST)
            new_form_obj = form.save(commit=False)
            new_form_obj.user = request.user
            new_form_obj.save()
            return redirect('todo:homedef')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': CreateForm(),
                                                            'errormessage': 'Bad Data. Please check the integrity.',
                                                            'updatemode': False, 'todo_id': 0})


def showtodo(request, todo_pk):
    todo_obj = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': CreateForm(instance=todo_obj),
                                                        'updatemode': True, 'todo_id': todo_pk})
    elif request.method == 'POST':
        try:
            form = CreateForm(request.POST, instance=todo_obj)
            form.save()
            return redirect('todo:homedef')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': CreateForm(),
                                                            'errormessage': 'Bad Data. Please check the integrity.',
                                                            'updatemode': True, 'todo_id': todo_pk})


def setcomplete(request, todo_pk):
    if request.method == 'POST':
        todo_obj = get_object_or_404(Todo, pk=todo_pk, user=request.user)
        todo_obj.datecompleted = timezone.now()
        todo_obj.save()
        return redirect('todo:homedef')


def delete_record(request, todo_pk):
    if request.method == 'POST':
        todo_obj = get_object_or_404(Todo, pk=todo_pk, user=request.user)
        todo_obj.delete()
        return redirect('todo:homedef')
