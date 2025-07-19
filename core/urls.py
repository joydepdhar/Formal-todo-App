from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/create/', views.task_create, name='task-create'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task-delete'),
    path('tasks/<int:task_id>/subtasks/', views.subtask_list, name='subtask-list'),
    path('tasks/<int:task_id>/subtasks/create/', views.subtask_create, name='subtask-create'),
    path('subtasks/<int:pk>/update/', views.subtask_update, name='subtask-update'),
    path('subtasks/<int:pk>/delete/', views.subtask_delete, name='subtask-delete'),
]
