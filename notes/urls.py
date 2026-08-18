from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('search-api/', views.note_search_api, name='note_search_api'),
    path('add/', views.note_create, name='note_create'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('<int:pk>/edit/', views.note_update, name='note_update'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
