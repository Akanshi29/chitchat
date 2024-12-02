from django.contrib import admin
from account.models import UserProfile, ProfilePhoto, Contacts
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ProfilePhoto)
admin.site.register(Contacts)