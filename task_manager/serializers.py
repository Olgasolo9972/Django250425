from rest_framework import serializers
from django.contrib.auth.models import User
from task_manager.models import Task, SubTask, Category


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'task_count']

    def get_task_count(self, obj):
        return obj.tasks.count()


# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'categories',
            'status', 'deadline', 'created_at', 'owner'
        ]
        read_only_fields = ['created_at', 'owner']


class TaskDetailSerializer(TaskSerializer):
    subtasks = serializers.SerializerMethodField(read_only=True)

    def get_subtasks(self, obj):
        from .serializers import SubTaskSerializer
        return SubTaskSerializer(obj.subtasks.all(), many=True).data


# SubTask Serializer
class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SubTask
        fields = [
            'id', 'title', 'description', 'task',
            'status', 'deadline', 'created_at', 'owner'
        ]
        read_only_fields = ['created_at', 'owner']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")

        if len(data["password"]) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)
