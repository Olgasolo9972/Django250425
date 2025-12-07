from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from task_manager.models import Task, SubTask, Category
from task_manager.serializers import TaskSerializer, TaskDetailSerializer, SubTaskSerializer, CategorySerializer

#HW_16
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get']) #HW_16
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.tasks.count()
        return Response({'category': category.name, 'task_count': count})

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
