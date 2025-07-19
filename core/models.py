from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# ------------------------
# Task Model
# ------------------------
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    alert_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def is_overdue(self):
        return not self.is_completed and timezone.now() > self.deadline

    def send_deadline_alert(self):
        if not self.alert_sent and self.deadline - timezone.now() <= timedelta(hours=1):
            self.alert_sent = True
            self.save()
            # Add your email or notification logic here
            return True
        return False


# ------------------------
# SubTask Model
# ------------------------
class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    alert_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} -> {self.task.title}"

    def is_overdue(self):
        return not self.is_completed and timezone.now() > self.deadline

    def send_deadline_alert(self):
        if not self.alert_sent and self.deadline - timezone.now() <= timedelta(hours=1):
            self.alert_sent = True
            self.save()
            return True
        return False
