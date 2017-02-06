from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	num_urgent_pr = models.PositiveSmallIntegerField(null=False, blank=False, default=6, verbose_name='Number of urgent prayer requests on today page')
	num_normal_pr = models.PositiveSmallIntegerField(null=False, blank=False, default=6, verbose_name='Number of simple prayer requests on today page')


class PrayerRequest(models.Model):
	id = models.BigAutoField(primary_key=True)
	title = models.CharField(max_length=255, null=False, blank=False)
	description = models.TextField(null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add=True, editable=False)
	deleted_date = models.DateTimeField(null=True)
	is_urgent = models.BooleanField(default=False)
	is_public = models.BooleanField(default=False)
	show_date = models.DateField(null=True, blank=True)
	created_by = models.ForeignKey(Profile, editable=False)


	def __str__(self):
		return self.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()