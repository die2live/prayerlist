from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template, Context
from django.http import HttpResponse
import datetime

from . import models
from . import forms
from social.apps.django_app.default.models import UserSocialAuth

@login_required
def index(request):
	prs = models.PrayerRequest.objects.all()
	return render(
		request, 
		'index.html',
		{
			'prayer_requests': prs,
		}
	)

@login_required
def edit(request, id):
    if request.method == 'GET':        
        print('LOG :: get')
        print('LOG :: %s' % id)
        #form = None
        if id:            
            print('LOG :: completed form')
            pr = get_object_or_404(models.PrayerRequest, pk=id)
            print('LOG :: %s' % pr)
            form = forms.EditPrayerRequestForm(instance=pr)
        else:
            print('LOG :: empty form')
            form = forms.EditPrayerRequestForm()        
        return render(request, 'create.html', {'form': form})
    elif request.method == 'POST':
        form = forms.EditPrayerRequestForm(request.POST)
        if form.is_valid():
            pr = form.save()
            return redirect('index')
        else:
            return render(request, 'create.html', {'form': form})        

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})