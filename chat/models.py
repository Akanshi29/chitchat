from django.db import models
from account.models import Contacts, UserProfile
import uuid

# Create your models here.
class Group(models.Model):
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile,related_name='group_members')
    title = models.TextField(null=True, blank=True)
    chat_type_choices = [
        ('1on1', '1on1'),
        ('group', 'Group'),
    ]
    chat_type = models.CharField(max_length=5, choices=chat_type_choices)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class ChatDetail(models.Model):
    message = models.TextField(null=False, blank=False)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message