from django import forms
from wetravel.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('region',)

class ProfileImageForm(forms.Form):
    """Image upload form"""
    image = forms.ImageField()

class PostForm(forms.Form):
	text = forms.CharField()
	post_image = forms.FileField()

