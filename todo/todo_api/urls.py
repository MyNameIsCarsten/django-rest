from django.urls import path, include
from .views import (
    TodoListApiView,
    TodoDetailApiView
)

urlpatterns = [
    # Create an endpoint for the class-based view
    path('api/', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
]