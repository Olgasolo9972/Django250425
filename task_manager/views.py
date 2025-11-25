from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from task_manager.models import Task
from task_manager.serializers import TaskSerializer


# Задание 1: Создание задачи
@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Задание 2: Список задач
@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# Задание 2: Конкретная задача
@api_view(['GET'])
def get_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


# Задание 3: Статистика
@api_view(['GET'])
def task_stats(request):
    total_tasks = Task.objects.count()

    status_stats = (
        Task.objects
        .values("status")
        .annotate(count=Count("status"))
    )

    overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()

    return Response({
        "total_tasks": total_tasks,
        "status_stats": status_stats,
        "overdue_tasks": overdue_tasks,
    })
