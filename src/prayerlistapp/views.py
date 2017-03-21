from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import PrayerRequest
from .forms import EditPrayerRequestForm, EditUserForm, EditProfileForm
from social.apps.django_app.default.models import UserSocialAuth


def index(request):       
    prs = PrayerRequest.objects.filter(
                    Q(is_public=True),
                    Q(show_date=datetime.today()) | 
                    Q(show_date=None))[:10]

    for pr in prs:
        pr.show_count += 1
        pr.save()

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
    prs = PrayerRequest.objects.filter(created_by=request.user.profile)
    return render(
		request, 
		'all.html',
		{
			'prayer_requests': prs,
		}
	)


@login_required
def today(request):     
    prs = PrayerRequest.objects.filter(Q(created_by=request.user.profile), Q(show_date=datetime.today()) | Q(show_date=None))[:request.user.profile.num_normal_pr]
    return render(
        request, 
        'today.html',
        {
            'prayer_requests': prs,            
        }
    )


@login_required
def edit(request, pk):    
    id = pk
    if request.method == 'GET':                
        if id:            
            pr = get_object_or_404(PrayerRequest, pk=id)
            form = EditPrayerRequestForm(instance=pr)
        else:
            form = EditPrayerRequestForm()
        return render(request, 'create.html', {'form': form, 'pr_id': id})
    elif request.method == 'POST':       
        id = pk if pk else request.POST['id']         
        if id:
            pr = get_object_or_404(PrayerRequest, pk=id)
            form = EditPrayerRequestForm(request.POST, instance=pr)
            if form.is_valid():                
                form.save()
                messages.add_message(request, messages.INFO, _('Your prayer request was updated.'))
            else:
                return render(request, 'create.html', {'form': form, 'pr_id': id})               
        else:   
            new_form = EditPrayerRequestForm(request.POST)
            new_pr = new_form.save(commit=False)            
            new_pr.created_by = request.user.profile
            new_pr.save()

            messages.add_message(request, messages.INFO, _('Your prayer request was saved.'))
        return redirect('/all/')
            


@login_required
@require_POST
def delete(request, id):
    pr = get_object_or_404(PrayerRequest, pk=id)
    pr.delete()
    messages.add_message(request, messages.INFO, _('Your prayer request was deleted.'))
    return HttpResponse('OK')

@login_required
@require_POST
def mark_as_read(request, id):
    pr = get_object_or_404(PrayerRequest, pk=id)
    pr.toggle_read()
    return HttpResponse('OK')

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('prayer:settings')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

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
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})