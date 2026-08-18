from django import forms
from .models import Task, Subject, StudySession


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'subject', 'due_date', 'priority', 'is_completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        self.fields['subject'].required = False


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'color']
        widgets = {'color': forms.TextInput(attrs={'type': 'color'})}


class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['subject', 'task', 'started_at', 'duration_minutes', 'notes']
        widgets = {
            'started_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
            self.fields['task'].queryset = Task.objects.filter(user=user)
