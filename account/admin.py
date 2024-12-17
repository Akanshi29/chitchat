from django.contrib import admin
from account.models import UserProfile, Contacts
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Contacts)