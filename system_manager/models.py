from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="inactive")

    # A trick to force a single record in the table
    singleton_enforcer = models.BooleanField(default=True, unique=True)

    def __str__(self):
        return "Site Notification"