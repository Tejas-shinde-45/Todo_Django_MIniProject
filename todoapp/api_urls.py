from django.urls import path
from . import api_views

urlpatterns = [
    path('todos/', api_views.todo_list_create),
    path('todos/<int:todo_id>/', api_views.todo_detail),
    path('login/', api_views.login_api)
]
