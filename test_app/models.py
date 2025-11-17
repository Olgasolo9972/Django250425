from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=120)  # VARCHAR
    description = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return f"Book '{self.title}'  -- Author '{self.author}'"

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=120, null=True, blank=True)

class UserProfile(models.Model):
    nickname = models.CharField(max_length=120, unique=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=120, null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    engagement_rate = models.FloatField(default=0)