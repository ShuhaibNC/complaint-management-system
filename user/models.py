from django.db import models

class SignupRecord(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=150, null=True, default="user")

    def __str__(self):
        return self.username

class Complaint(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    date_of_incident = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="complaints/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"