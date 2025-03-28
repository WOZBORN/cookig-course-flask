from django.db import models
from django.utils import timezone


class Enrollment(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=120)
    phone = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.fullname} - {self.email}"


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.order}: {self.title}"
