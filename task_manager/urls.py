from django.urls import path
from task_manager.views import create_task, list_tasks, get_task, task_stats

urlpatterns = [
    path('tasks/create/', create_task, name='task-create'),
    path('tasks/', list_tasks, name='task-list'),
    path('tasks/<int:id>/', get_task, name='task-detail'),
    path('tasks/stats/', task_stats, name='task-stats'),
]
