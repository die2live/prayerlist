from django import forms
from django.forms import ModelForm

from .models import PrayerRequest

class EditPrayerRequestForm(ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['title', 'description', 'is_urgent', 'is_public']