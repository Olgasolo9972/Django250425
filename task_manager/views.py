from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from task_manager.models import Task, SubTask
from .serializers import TaskDetailSerializer, SubTaskSerializer


# Задание 1: Фильтр задач по дню недели
class TaskByWeekdayView(APIView):
    def get(self, request):
        weekday_param = request.query_params.get('weekday', None)
        tasks = Task.objects.all()

        if weekday_param:
            weekday_param = weekday_param.lower()
            days = {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6
            }
            day_index = days.get(weekday_param)
            if day_index is not None:
                tasks = tasks.filter(deadline__week_day=(day_index + 1))
            else:
                return Response({"error": "Invalid weekday"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data)


# Задание 2: Пагинация подзадач
class SubTaskPagination(PageNumberPagination):
    page_size = 5
    ordering = '-created_at'


class SubTaskListView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all().order_by('-created_at')
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# Задание 3: Фильтр подзадач по задаче и статусу
class SubTaskFilterView(APIView):
    def get(self, request):
        task_name = request.query_params.get('task_name', None)
        status_param = request.query_params.get('status', None)

        subtasks = SubTask.objects.all().order_by('-created_at')

        if task_name:
            subtasks = subtasks.filter(task__title__icontains=task_name)
        if status_param:
            subtasks = subtasks.filter(status=status_param)

        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
