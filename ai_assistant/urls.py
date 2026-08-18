from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.ai_home, name='home'),
    path('chat/', views.ai_chat, name='chat'),
    path('summarize/', views.ai_summarize, name='summarize'),
    path('summarize/<int:note_pk>/', views.ai_summarize, name='summarize_note'),
    path('quiz/', views.ai_quiz, name='quiz'),
    path('flashcards/', views.ai_flashcards, name='flashcards'),
    path('explain-error/', views.ai_explain_error, name='explain_error'),
]
