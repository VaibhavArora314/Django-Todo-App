from django.urls import path
from . import views

urlpatterns = [
    path('',views.TaskList.as_view(), name='tasks'),
    path('task-create/',views.TaskCreate.as_view(), name='task-create'),
    path('task-edit/<int:pk>',views.TaskUpdate.as_view(), name='task-edit'),
    path('task-delete/<int:pk>',views.TaskDelete.as_view(), name='task-delete'),
    path('task-mark-complete/<int:pk>',views.TaskMarkComplete.as_view(), name='task-mark-complete'),
    path('task-mark-incomplete/<int:pk>',views.TaskMarkIncomplete.as_view(), name='task-mark-incomplete')
]
