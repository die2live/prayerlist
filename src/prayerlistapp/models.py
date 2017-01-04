from django.db import models

class PrayerRequest(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(null=True)
	created_date = models.DateTimeField(auto_now_add=True)

