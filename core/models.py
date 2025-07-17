from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    alert_sent = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    alert_sent = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.title} (Subtask of {self.task.title})"

    class Meta:
        ordering = ['deadline']
