from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['resource_type', 'title', 'description', 'category', 'available_quantity', 'unit', 'urgency', 'delivery_method', 'pickup_window', 'image', 'latitude', 'longitude']
        widgets = {
            'resource_type': forms.RadioSelect(attrs={'class': 'type-selector'}),
            'delivery_method': forms.Select(attrs={'class': 'urgency-select'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'urgency': forms.Select(attrs={'class': 'urgency-select'}),
        }
        help_texts = {
            'latitude': 'Auto-detected if you enable location.',
            'longitude': 'Auto-detected if you enable location.',
        }
