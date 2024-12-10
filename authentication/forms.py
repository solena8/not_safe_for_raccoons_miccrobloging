from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from .models import Profile

from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

# Formulaire pour la mise à jour des informations utilisateur et du profil
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Profile  
        
        fields = ['avatar']  

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            pass
        return avatar
        

# for profile update
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        
       