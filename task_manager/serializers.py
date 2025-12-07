from rest_framework import serializers
from django.utils import timezone
from task_manager.models import Task, SubTask, Category

#HW_16
class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'task_count']

    def get_task_count(self, obj):
        return obj.tasks.count()  # количество задач в категории

# Task сериализаторы
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') #HW_19
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['created_at', 'owner']


class TaskDetailSerializer(TaskSerializer):
    subtasks = serializers.SerializerMethodField(read_only=True)

    def get_subtasks(self, obj):
        from .serializers import SubTaskSerializer
        subtasks = obj.subtasks.all()
        return SubTaskSerializer(subtasks, many=True).data


# SubTask сериализаторы
class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') #HW_19
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['created_at', 'owner']

