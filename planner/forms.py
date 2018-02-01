from django import forms

from .models import Note

class DeleteNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = []

class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'expr_date']
