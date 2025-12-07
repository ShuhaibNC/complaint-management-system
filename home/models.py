from django.db import models

from django.contrib.auth.models import User

class SOSAlert(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS from {self.username} at {self.latitude}, {self.longitude}"
    
class Feedback(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.id}"

