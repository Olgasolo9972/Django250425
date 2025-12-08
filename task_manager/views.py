from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from task_manager.models import Task, SubTask, Category
from task_manager.serializers import TaskSerializer, TaskDetailSerializer, SubTaskSerializer, CategorySerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
#HW_20
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

#HW_20
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

#HW_20
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh = request.data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "Logged out"}, status=200)
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=400)


# Custom permission: только владелец может изменять/удалять объект
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny] #HW_20

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.tasks.count()
        return Response({'category': category.name, 'task_count': count})


# Task Views
class TaskListCreateGenericView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Пользователь видит только свои задачи
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyGenericView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Ограничиваем доступ к задачам только владельцем
        return Task.objects.filter(owner=self.request.user)


# SubTask Views
class SubTaskListCreateGenericView(generics.ListCreateAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskRetrieveUpdateDestroyGenericView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)


# View для получения задач текущего пользователя
class MyTasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')
