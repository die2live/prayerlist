from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	id = models.BigAutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	num_urgent_pr = models.PositiveSmallIntegerField(null=False, blank=False, default=6, verbose_name='Number of urgent prayer requests on today page')
	num_normal_pr = models.PositiveSmallIntegerField(null=False, blank=False, default=6, verbose_name='Number of simple prayer requests on today page')
	
	def __str__(self):
		return self.user.email


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


class UserGroup(models.Model):
	id = models.BigAutoField(primary_key=True)
	created_by = models.ForeignKey(Profile, editable=False, related_name='%(class)s_createdby')
	users = models.ManyToManyField(Profile, related_name='%(class)s_usersattached')	
	name = models.CharField(max_length=255, null=False, blank=False)

	def __str__(self):
		return self.name



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.create(user=instance)
		
		pr1 = PrayerRequest(
			title='Pray for a specific individual',
			description = 'Perhaps a person you know well, or even someone you have just met today. We know so many who still need God’s salvation. Pray earnestly for their soul, that God will deal with them as he has with us. We probably little realize how many prayed for us.',
			created_by = profile
		)
		pr1.save()
		pr2 = PrayerRequest(
			title='Pray for a missionary or evangelist',
			description = 'Many men and women have left family and friend behind to go forth and preach the message of God’s salvation. They need our prayers as they face difficulties we may never experience. Pray regularly for them by name, asking God to meet their specific needs.',
			created_by = profile
		)
		pr2.save()
		pr3 = PrayerRequest(
			title='Pray for an area of need',
			description = 'It may be a country far away, or a little town nearby. Remember the multitudes in need, many of whom don’t have the privilege of hearing the gospel message preached. Ask God to raise up those to go among them and present Christ as Saviour.',
			created_by = profile
		)
		pr3.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()