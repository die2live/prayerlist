from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template, Context
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from datetime import datetime

from . import models
from . import forms
from social.apps.django_app.default.models import UserSocialAuth

def index(request):   
    prs = models.PrayerRequest.objects.all()
    return render(
        request, 
        'index.html',
        {
            'prayer_requests': prs,
        }
    )


def about(request):       
    return render(
        request, 
        'about.html',
        {}
    )


@login_required
def all(request):	
    prs = models.PrayerRequest.objects.filter(created_by=request.user.profile)
    return render(
		request, 
		'all.html',
		{
			'prayer_requests': prs,
		}
	)


@login_required
def today(request): 
    uprs = models.PrayerRequest.objects.filter(Q(created_by=request.user.profile), Q(is_urgent=True), Q(show_date=datetime.today()) | Q(show_date=None)).order_by('-created_date')[:request.user.profile.num_urgent_pr]
    prs = models.PrayerRequest.objects.filter(Q(created_by=request.user.profile), Q(is_urgent=False), Q(show_date=datetime.today()) | Q(show_date=None)).order_by('-created_date')[:request.user.profile.num_normal_pr]
    return render(
        request, 
        'today.html',
        {
            'prayer_requests': prs,
            'urgent_prayer_requests': uprs,
        }
    )


@login_required
def edit(request, pk):    
    id = pk
    if request.method == 'GET':                
        if id:            
            pr = get_object_or_404(models.PrayerRequest, pk=id)
            form = forms.EditPrayerRequestForm(instance=pr)
        else:
            form = forms.EditPrayerRequestForm()
        return render(request, 'create.html', {'form': form, 'pr_id': id})
    elif request.method == 'POST':       
        id = pk if pk else request.POST['id']         
        if id:
            pr = get_object_or_404(models.PrayerRequest, pk=id)            
            form = forms.EditPrayerRequestForm(request.POST, instance=pr)                    
            if form.is_valid():                        
                #pr.title = form.cleaned_data['title']
                #pr.description = form.cleaned_data['description']
                #pr.is_urgent = form.cleaned_data['is_urgent']
                #pr.is_public = form.cleaned_data['is_public']
                #pr.created_by = request.user.profile
                #pr.save()
                form.save()
                messages.add_message(request, messages.INFO, 'Your prayer request was updated.')
            else:
                return render(request, 'create.html', {'form': form, 'pr_id': id})               
        else:   
            new_form = forms.EditPrayerRequestForm(request.POST)
            new_pr = new_form.save(commit=False)            
            new_pr.created_by = request.user.profile
            new_pr.save()                            
            messages.add_message(request, messages.INFO, 'Your prayer request was saved.')              
        return redirect('/all/')
            


@login_required
@require_POST
def delete(request, id):
    pr = get_object_or_404(models.PrayerRequest, pk=id)
    pr.delete()
    messages.add_message(request, messages.INFO, 'Your prayer request was deleted.')
    return HttpResponse('OK')

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = forms.EditUserForm(request.POST, instance=request.user)
        profile_form = forms.EditProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('prayer:settings')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = forms.EditUserForm(instance=request.user)
        profile_form = forms.EditProfileForm(instance=request.user.profile)

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

        try:
            google_login = user.social_auth.get(provider='google-oauth2')
        except UserSocialAuth.DoesNotExist:
            google_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'google_login': google_login,
        'can_disconnect': can_disconnect,        
        'profile_form': profile_form,
        'user_form': user_form
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