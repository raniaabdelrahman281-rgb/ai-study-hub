from django import forms
from .models import Note, Category
from planner.models import Subject


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'subject', 'categories', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
            self.fields['categories'].queryset = Category.objects.filter(user=user)
        self.fields['subject'].required = False


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
