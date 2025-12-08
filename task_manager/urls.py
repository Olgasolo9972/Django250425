from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_manager.views import (
    TaskListCreateGenericView,
    TaskRetrieveUpdateDestroyGenericView,
    SubTaskListCreateGenericView,
    SubTaskRetrieveUpdateDestroyGenericView,
    CategoryViewSet,
    MyTasksListView,
    RegisterView, #HW_20
    LogoutView, #HW_20
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



# Swagger setup
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router for categories
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Generic Views для задач
    path('tasks/', TaskListCreateGenericView.as_view(), name='task-list-create-generic'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyGenericView.as_view(), name='task-detail-generic'),

    # Generic Views для подзадач
    path('subtasks/', SubTaskListCreateGenericView.as_view(), name='subtask-list-create-generic'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyGenericView.as_view(), name='subtask-detail-generic'),

    # Категории через Router
    path('', include(router.urls)),

    # JWT токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger / Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Задачи текущего пользователя
    path('my-tasks/', MyTasksListView.as_view(), name='my-tasks'),

    #HW_20
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

]
