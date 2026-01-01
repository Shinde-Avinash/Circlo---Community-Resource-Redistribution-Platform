from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phone_number', 'latitude', 'longitude')
        widgets = {
            'role': forms.Select(attrs={'class': 'modern-input'}),
        }
        help_texts = {
            'latitude': 'Optional: Auto-detected in full app',
            'longitude': 'Optional: Auto-detected in full app',
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'email', 'phone_number', 'latitude', 'longitude']
        widgets = {
             'latitude': forms.TextInput(attrs={'placeholder': 'Latitude'}),
             'longitude': forms.TextInput(attrs={'placeholder': 'Longitude'}),
        }

class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_verified', 'phone_number', 'profile_image']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
