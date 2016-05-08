from django.contrib.auth.models import User
from django import forms

from models import Album,Songs

from django.contrib import messages



class UserForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput)
    password1=forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model=User
        fields=['username','email','password','password1']



class LoginForm(forms.Form):
    username=forms.CharField(max_length=250)
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:

        fields=['username','password']



class AlbumForm(forms.ModelForm):

    class Meta:
      model=Album
      fields=['artist','album_title','genre','album_logo']



class SongsForm(forms.ModelForm):
    class Meta:
        model=Songs
        fields=['song_title','file_type','release_date','music_file']
