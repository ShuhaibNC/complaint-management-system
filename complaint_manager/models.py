from django.db import models

# Create your models here.

class Complaint(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=30, blank=True)
    description = models.TextField()
    date_of_incident = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="complaints/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='recieved')
    forward = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"