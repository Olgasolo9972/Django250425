from django.urls import path
from task_manager.views import (
    TaskListCreateGenericView,
    TaskRetrieveUpdateDestroyGenericView,
    SubTaskListCreateGenericView,
    SubTaskRetrieveUpdateDestroyGenericView,
)

urlpatterns = [
    # Generic Views для задач
    path('tasks/', TaskListCreateGenericView.as_view(), name='task-list-create-generic'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyGenericView.as_view(), name='task-detail-generic'),

    # Generic Views для подзадач
    path('subtasks/', SubTaskListCreateGenericView.as_view(), name='subtask-list-create-generic'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyGenericView.as_view(), name='subtask-detail-generic'),
]
