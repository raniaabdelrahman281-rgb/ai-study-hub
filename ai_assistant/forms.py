from django import forms
from .models import AIConversation


class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask me anything about your studies...'}))


class SummarizeForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), label='Text to summarize')


class QuizForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), label='Study material')
    num_questions = forms.IntegerField(min_value=1, max_value=15, initial=5)


class FlashcardForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), label='Study material')
    num_cards = forms.IntegerField(min_value=1, max_value=20, initial=8)


class ExplainErrorForm(forms.Form):
    error_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}), label='Paste your error message')
