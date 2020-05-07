from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import Post
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('image', 'title', 'bio', 'location', 'phone_number',)