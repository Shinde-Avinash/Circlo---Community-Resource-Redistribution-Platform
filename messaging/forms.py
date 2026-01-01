from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Type a message...',
                'autocomplete': 'off',
                'style': 'width: 100%; padding: 0.8rem; border: 1px solid var(--border-color); border-radius: 20px;'
            })
        }
