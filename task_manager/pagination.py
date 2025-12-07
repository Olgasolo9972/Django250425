#HW_17
from rest_framework.pagination import CursorPagination

class TaskCursorPagination(CursorPagination):
    page_size = 6                # максимум объектов на странице
    ordering = '-created_at'      # сортировка по убыванию даты создания
    cursor_query_param = 'cursor'
