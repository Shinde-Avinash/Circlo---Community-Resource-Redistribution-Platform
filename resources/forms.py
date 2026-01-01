from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'category', 'available_quantity', 'unit', 'urgency', 'pickup_window', 'image', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'urgency': forms.Select(attrs={'class': 'urgency-select'}),
        }
        help_texts = {
            'latitude': 'Auto-detected if you enable location.',
            'longitude': 'Auto-detected if you enable location.',
        }
