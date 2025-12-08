from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'

    # HW_21
    def ready(self):
        import task_manager.signals
