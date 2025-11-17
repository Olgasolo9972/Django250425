from django.db import models


STATUS_CHOICES = [
    ("new", "new"),
    ("progress", "progress"),
    ("pending", "pending"),
    ("blocked", "blocked"),
    ("done", "done"),
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("title", "created_at")  # уникально для даты создания

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} -- {self.title}"
