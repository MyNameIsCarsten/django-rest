from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import Todo
from .serializers import TodoSerializer
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

from .forms import TodoForm  

@login_required
def contact(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            task=request.POST.get('task')
            user = request.user

            newtodo = Todo(task=task, user=user)
            newtodo.save()
            data = {'task':task, 'user': user.username}
            print(data)
            return JsonResponse(data, safe=False)
    
        
    else:
        form = TodoForm()

    return render(request, 'todo_api/contact.html', {'form': form})

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # fetches all the objects from the model by filtering with the requested user ID
        todos = Todo.objects.filter(user = request.user.id)

        # serializes from the model object to a JSON serialized object
        serializer = TodoSerializer(todos, many=True)

        # returns the response with serialized data and status as 200_OK
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        # fetches the requested data and adds the requested user ID in the data dictionary
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }

        # creates a serialized object
        serializer = TodoSerializer(data=data)

        # saves the object if it’s valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    
    def get_object(self, todo_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Todo.objects.get(id=todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        # fetches the object with the ID todo_id and user as request user from the to-do model
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # serializes the model object to a JSON serialized object
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        # fetches the to-do object if it is available in the database
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # updates its data with requested data
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)

        # saves the updated data in the database
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        # fetches the to-do object if is available in the database
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # deletes it
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
