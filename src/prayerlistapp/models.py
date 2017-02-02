from django.db import models

class PrayerRequest(models.Model):
	id = models.BigAutoField(primary_key=True)
	title = models.CharField(max_length=255, null=False, blank=False)
	description = models.TextField(null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add=True, editable=False)
	deleted_date = models.DateTimeField(null=True)
	is_urgent = models.BooleanField(default=False)
	is_public = models.BooleanField(default=False)
	show_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.title

