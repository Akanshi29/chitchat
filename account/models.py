# account/models.py
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_mobile_number


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=False, blank=False, unique=True, validators=[validate_mobile_number])

    REQUIRED_FIELDS = ["username", "first_name", "last_name"] 
    
    def __str__(self):
        return self.user.username


class ProfilePhoto(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Contacts(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=15, null=False, blank=False, unique=True)
    mobile_number = models.CharField(max_length=15, null=False, blank=False, unique=True, validators=[validate_mobile_number])
    chat_initated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
