from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_manager.views import (
    TaskListCreateGenericView,
    TaskRetrieveUpdateDestroyGenericView,
    SubTaskListCreateGenericView,
    SubTaskRetrieveUpdateDestroyGenericView,
    CategoryViewSet,
)
#HW_18
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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

    # Category Router
    path('', include(router.urls)),

    # JWT токены #HW_18
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
