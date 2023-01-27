from django import forms
from board.models import Message, Comment

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['message', 'user']