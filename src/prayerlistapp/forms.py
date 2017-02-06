from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput, TextInput, Textarea, NumberInput, EmailInput

from .models import PrayerRequest, Profile

class EditPrayerRequestForm(ModelForm):

	class Meta:
		model = PrayerRequest
		fields = ['id', 'title', 'description', 'is_urgent', 'is_public', 'show_date']
		#exclude = ['created_by']
		widgets = {
				'title': TextInput(attrs={'class':'form-control'}),
				'description': Textarea(attrs={'class':'form-control'}),
				'show_date': DateInput(attrs={'class':'form-control datepicker'}),
		}


class EditProfileForm(ModelForm):

	class Meta:
		model = Profile
		fields = ['id', 'num_urgent_pr', 'num_normal_pr']		
		widgets = {
				'num_urgent_pr': NumberInput(attrs={'class':'form-control'}),				
				'num_normal_pr': NumberInput(attrs={'class':'form-control'}),
		}


class EditUserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		widgets = {
				'first_name': TextInput(attrs={'class':'form-control'}),
				'last_name': TextInput(attrs={'class':'form-control'}),
				'email': EmailInput(attrs={'class':'form-control'}),
		}