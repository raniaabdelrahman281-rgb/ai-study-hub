from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ChatForm, SummarizeForm, QuizForm, FlashcardForm, ExplainErrorForm
from .models import AIConversation
from .services import (
    chat_reply, summarize_text, generate_quiz, generate_flashcards, explain_error, AIServiceError
)
from notes.models import Note


@login_required
def ai_home(request):
    conversations = AIConversation.objects.filter(user=request.user)[:10]
    return render(request, 'ai_assistant/home.html', {'conversations': conversations})


@login_required
def ai_chat(request):
    reply = None
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            try:
                reply = chat_reply(message)
                AIConversation.objects.create(user=request.user, feature='chat', prompt=message, response=reply)
            except AIServiceError as exc:
                messages.error(request, str(exc))
    else:
        form = ChatForm()
    history = AIConversation.objects.filter(user=request.user, feature='chat')[:20]
    return render(request, 'ai_assistant/chat.html', {'form': form, 'reply': reply, 'history': history})


@login_required
def ai_summarize(request, note_pk=None):
    note = None
    initial = {}
    if note_pk:
        note = get_object_or_404(Note, pk=note_pk, user=request.user)
        initial = {'text': note.content}

    result = None
    if request.method == 'POST':
        form = SummarizeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                result = summarize_text(text)
                AIConversation.objects.create(
                    user=request.user, note=note, feature='summarize', prompt=text, response=result
                )
                if note:
                    note.ai_summary = result
                    note.save(update_fields=['ai_summary'])
                messages.success(request, 'Summary generated.')
            except AIServiceError as exc:
                messages.error(request, str(exc))
    else:
        form = SummarizeForm(initial=initial)
    return render(request, 'ai_assistant/summarize.html', {'form': form, 'result': result, 'note': note})


@login_required
def ai_quiz(request):
    result = None
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            n = form.cleaned_data['num_questions']
            try:
                result = generate_quiz(text, n)
                AIConversation.objects.create(user=request.user, feature='quiz', prompt=text, response=result)
            except AIServiceError as exc:
                messages.error(request, str(exc))
    else:
        form = QuizForm()
    return render(request, 'ai_assistant/quiz.html', {'form': form, 'result': result})


@login_required
def ai_flashcards(request):
    result = None
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            n = form.cleaned_data['num_cards']
            try:
                result = generate_flashcards(text, n)
                AIConversation.objects.create(user=request.user, feature='flashcards', prompt=text, response=result)
            except AIServiceError as exc:
                messages.error(request, str(exc))
    else:
        form = FlashcardForm()
    return render(request, 'ai_assistant/flashcards.html', {'form': form, 'result': result})


@login_required
def ai_explain_error(request):
    result = None
    if request.method == 'POST':
        form = ExplainErrorForm(request.POST)
        if form.is_valid():
            error_text = form.cleaned_data['error_text']
            try:
                result = explain_error(error_text)
                AIConversation.objects.create(
                    user=request.user, feature='explain_error', prompt=error_text, response=result
                )
            except AIServiceError as exc:
                messages.error(request, str(exc))
    else:
        form = ExplainErrorForm()
    return render(request, 'ai_assistant/explain_error.html', {'form': form, 'result': result})
