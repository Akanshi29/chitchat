# account/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, ProfilePhoto
from .validators import validate_mobile_number  # Import the custom validator

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Apply the custom validator for mobile_number
    mobile_number = forms.CharField(
        max_length=15,
        required=True,
        validators=[validate_mobile_number]  # Use the custom validator here
    )
    
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        # Check if user with the same username exists
        existing_user = User.objects.filter(username=self.cleaned_data.get('username')).exists()
        if not existing_user:
            # Save the user first
            user = super().save(commit=False)
            if commit:
                user.save()

        # Create and save the user's profile
        profile = UserProfile.objects.create(
            user=user,
            birthday=self.cleaned_data['birthday'],
            mobile_number=self.cleaned_data['mobile_number']
        )
        profile_photo = ProfilePhoto.objects.create(
            user=profile,
            profile_photo=self.cleaned_data['profile_photo']
        )

        return user
