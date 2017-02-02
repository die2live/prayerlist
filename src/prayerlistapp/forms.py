from django import forms
from django.forms import ModelForm, DateInput, TextInput, Textarea

from .models import PrayerRequest

class EditPrayerRequestForm(ModelForm):

	class Meta:
		model = PrayerRequest
		fields = ['id', 'title', 'description', 'is_urgent', 'is_public', 'show_date']
		widgets = {
				'title': TextInput(attrs={'class':'form-control'}),
				'description': Textarea(attrs={'class':'form-control'}),
				'show_date': DateInput(attrs={'class':'form-control datepicker'}),
		}