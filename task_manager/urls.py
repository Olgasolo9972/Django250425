from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_manager.views import (
    TaskListCreateGenericView,
    TaskRetrieveUpdateDestroyGenericView,
    SubTaskListCreateGenericView,
    SubTaskRetrieveUpdateDestroyGenericView,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Generic Views для задач
    path('tasks/', TaskListCreateGenericView.as_view(), name='task-list-create-generic'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyGenericView.as_view(), name='task-detail-generic'),

    # Generic Views для подзадач
    path('subtasks/', SubTaskListCreateGenericView.as_view(), name='subtask-list-create-generic'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyGenericView.as_view(), name='subtask-detail-generic'),

    # HW_16 Роутер для категорий
    path('', include(router.urls)),
]