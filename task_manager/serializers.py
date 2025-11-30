from rest_framework import serializers
from django.utils import timezone
from task_manager.models import Task, SubTask, Category

# SubTaskCreateSerializer
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)  # поле доступно только для чтения

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']


# CategoryCreateSerializer
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    # Переопределяем create для проверки уникальности
    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": "Категория с таким названием уже существует."})
        return super().create(validated_data)

    # Переопределяем update для проверки уникальности
    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"name": "Категория с таким названием уже существует."})
        return super().update(instance, validated_data)


# SubTaskSerializer для вложенности
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']


# TaskDetailSerializer
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)  # вложенный сериализатор

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'categories', 'subtasks']


# TaskCreateSerializer
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']

    # Валидация deadline
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
        return value
