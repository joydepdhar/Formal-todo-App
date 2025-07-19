from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


def check_and_update_task(task):
    if task.deadline < timezone.now() and task.is_completed:
        task.is_completed = False
        task.save()

def check_and_update_subtask(subtask):
    if subtask.deadline < timezone.now() and subtask.is_completed:
        subtask.is_completed = False
        subtask.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        check_and_update_task(task)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
        check_and_update_task(task)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def task_update(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
        check_and_update_task(task)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_delete(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    task.delete()
    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subtask_list(request, task_id):
    subtasks = SubTask.objects.filter(task__id=task_id, task__user=request.user)
    for subtask in subtasks:
        check_and_update_subtask(subtask)
    serializer = SubTaskSerializer(subtasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subtask_create(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['task'] = task.id
    serializer = SubTaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def subtask_update(request, pk):
    try:
        subtask = SubTask.objects.get(pk=pk, task__user=request.user)
        check_and_update_subtask(subtask)
    except SubTask.DoesNotExist:
        return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def subtask_delete(request, pk):
    try:
        subtask = SubTask.objects.get(pk=pk, task__user=request.user)
    except SubTask.DoesNotExist:
        return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
    subtask.delete()
    return Response({'message': 'Subtask deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
