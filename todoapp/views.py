from django.shortcuts import render,redirect,get_object_or_404
from .models import Todo
# Create your views here.

def home(request):
    todos=Todo.objects.all()

    if request.method == "POST":
        title=request.POST.get('title')
        description = request.POST.get('description')

        if title:
            Todo.objects.create(
                title=title,
                description=description
            )
        return redirect('home')
    
    return render(request,'todoapp/home.html',{'todos':todos})

def toggle_completed(request,todo_id):
    todo=get_object_or_404(Todo,id=todo_id)
    todo.completed=not todo.completed
    todo.save()
    return redirect('home')

def delete_todo(request,todo_id):
    todo=get_object_or_404(Todo,id=todo_id)
    todo.delete()
    return redirect('home')


def edit_todo(request,todo_id):
    todo=get_object_or_404(Todo,id=todo_id)

    if  request.method == "POST":
        todo.title=request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.save()
        return redirect('home')
    
    return render(request,'todoapp/edit.html',{'todo':todo})


