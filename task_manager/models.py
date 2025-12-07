from django.db import models
from django.utils import timezone


STATUS_CHOICES = [
    ("new", "new"),
    ("progress", "progress"),
    ("pending", "pending"),
    ("blocked", "blocked"),
    ("done", "done"),
]

class CategoryManager(models.Manager):
    def get_queryset(self):
        # возвращаем только активные категории
        return super().get_queryset().filter(is_deleted=False)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = CategoryManager()  # менеджер по умолчанию
    all_objects = models.Manager()  # обычный менеджер для доступа ко всем категориям

    def delete(self, using=None, keep_parents=False):
        # мягкое удаление
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-id"]  # по убыванию id
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_category_name")
        ]


class Task(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]  # сортировка по убыванию даты создания
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_task_title")
        ]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} -- {self.title}"

    class Meta:
        db_table = "task_manager_subtask"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_subtask_title")
        ]
