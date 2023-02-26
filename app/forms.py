from django import forms
from django.forms import ModelForm, TextInput, Select
from .models import UserSong


class UserSongForm(forms.ModelForm):
    class Meta:
        model = UserSong
        fields = '__all__'