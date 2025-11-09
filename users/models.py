from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Siswa'),
        ('instructor', 'Instruktur'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)                                                                                
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})