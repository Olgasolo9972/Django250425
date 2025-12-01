from django.urls import path
from task_manager.views import (
    TaskByWeekdayView,
    SubTaskListView,
    SubTaskFilterView,
)

urlpatterns = [
    path('tasks/by-weekday/', TaskByWeekdayView.as_view(), name='tasks-by-weekday'),
    path('subtasks/paginated/', SubTaskListView.as_view(), name='subtasks-paginated'),
    path('subtasks/filter/', SubTaskFilterView.as_view(), name='subtasks-filter'),
]
