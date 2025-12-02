from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from task_manager.models import Task, SubTask
from task_manager.serializers import TaskSerializer, TaskDetailSerializer, SubTaskSerializer

# Задание 1: Generic Views для задач
class TaskListCreateGenericView(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']  # фильтрация
    search_fields = ['title', 'description']   # поиск
    ordering_fields = ['created_at']          # сортировка
    ordering = ['-created_at']                # сортировка по умолчанию

class TaskRetrieveUpdateDestroyGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Задание 2: Generic Views для подзадач
class SubTaskListCreateGenericView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']  # фильтрация
    search_fields = ['title', 'description']   # поиск
    ordering_fields = ['created_at']           # сортировка
    ordering = ['-created_at']                 # сортировка по умолчанию

class SubTaskRetrieveUpdateDestroyGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
