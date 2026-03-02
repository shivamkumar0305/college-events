from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student','Student'),
        ('organizer', 'Organizer'),
        ('admin','Admin')
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)


    #for students 
    college = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True,blank=True)

    #organizer only 
    organization_name = models.CharField(max_length=200,blank=True)
    is_verified_organizer = models.BooleanField(default=False)

    #pfp
    profile_picture = models.ImageField(upload_to='profiles/', null=True,blank=True)
    bio = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
 
    def __str__(self):
        return self.email
