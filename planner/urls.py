from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('export/pdf/', views.task_export_pdf, name='task_export_pdf'),
    path('add/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/toggle/', views.task_toggle_complete, name='task_toggle_complete'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
]
