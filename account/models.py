# account/models.py
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_mobile_number


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=False, blank=False, unique=True, validators=[validate_mobile_number])
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    REQUIRED_FIELDS = ["username", "first_name", "last_name"] 
    
    def __str__(self):
        return self.user.username


class Contacts(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="member", null=True)
    name = models.CharField(max_length=15, null=True, blank=True, unique=True)
    chat_initated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.user_member.user.first_name
