import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Todo

import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import AuthToken

# for login
@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    body = json.loads(request.body)

    username = body.get("username")
    password = body.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Wrong username or password"}, status=401)

    token, created = AuthToken.objects.get_or_create(
        user=user,
        defaults={"token": str(uuid.uuid4())}
    )

    return JsonResponse({
        "message": "Login successful",
        "token": token.token
    })

@csrf_exempt
def todo_list_create(request):

    # GET → list all todos
    if request.method == "GET":
        todos = Todo.objects.all().order_by('-created_at')

        data = []
        for todo in todos:
            data.append({
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "created_at": todo.created_at,
            })

        return JsonResponse(data, safe=False, status=200)

    # POST → create todo
    elif request.method == "POST":
        try:
            body = json.loads(request.body)

            todo = Todo.objects.create(
                title=body.get("title"),
                description=body.get("description", "")
            )

            return JsonResponse({
                "id": todo.id,
                "message": "Todo created successfully"
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
def todo_detail(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return JsonResponse({"error": "Todo not found"}, status=404)

    # GET one todo
    if request.method == "GET":
        return JsonResponse({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at,
        })

    # PUT → update todo
    elif request.method == "PUT":
        body = json.loads(request.body)

        todo.title = body.get("title", todo.title)
        todo.description = body.get("description", todo.description)
        todo.completed = body.get("completed", todo.completed)
        todo.save()

        return JsonResponse({"message": "Todo updated"}, status=200)

    # DELETE → delete todo
    elif request.method == "DELETE":
        todo.delete()
        return JsonResponse({"message": "Todo deleted"}, status=204)
