from django.contrib import admin
from .models import Task, SubTask

# Inline SubTask in Task view
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0  # No extra blank rows
    fields = ('title', 'description', 'deadline', 'is_completed', 'alert_sent')
    readonly_fields = ('created_at',)

# Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'deadline', 'is_completed', 'alert_sent', 'created_at')
    list_filter = ('is_completed', 'alert_sent', 'deadline')
    search_fields = ('title', 'description', 'user__username')
    inlines = [SubTaskInline]
    readonly_fields = ('created_at',)

# SubTask Admin
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'deadline', 'is_completed', 'alert_sent', 'created_at')
    list_filter = ('is_completed', 'alert_sent', 'deadline')
    search_fields = ('title', 'description', 'task__title')
    readonly_fields = ('created_at',)
