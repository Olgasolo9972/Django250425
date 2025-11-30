from django.urls import path
from task_manager.views import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)


urlpatterns = [
    # path('tasks/create/', create_task, name='task-create'),
    # path('tasks/', list_tasks, name='task-list'),
    # path('tasks/<int:id>/', get_task, name='task-detail'),
    # path('tasks/stats/', task_stats, name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
