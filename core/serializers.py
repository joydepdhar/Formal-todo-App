from rest_framework import serializers
from .models import Task, SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            'id',
            'task',
            'title',
            'description',
            'created_at',
            'deadline',
            'is_completed',
            'alert_sent',
        ]
        read_only_fields = ['id', 'created_at', 'alert_sent']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)  # nested subtasks list

    class Meta:
        model = Task
        fields = [
            'id',
            'user',
            'title',
            'description',
            'created_at',
            'deadline',
            'is_completed',
            'alert_sent',
            'subtasks',
        ]
        read_only_fields = ['id', 'created_at', 'alert_sent', 'user']
