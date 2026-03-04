from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('toggle/<int:todo_id>/',views.toggle_completed,name='toggle_completed'),
    path('delete/<int:todo_id>/',views.delete_todo,name='delete_todo'),
    path('edit/<int:todo_id>/',views.edit_todo,name='edit_todo')
]
