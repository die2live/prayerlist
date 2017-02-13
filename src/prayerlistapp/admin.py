from django.contrib import admin

from .models import Profile, PrayerRequest, UserGroup

admin.site.register(Profile)
admin.site.register(UserGroup)
admin.site.register(PrayerRequest)
