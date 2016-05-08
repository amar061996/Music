from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models



class Album(models.Model):


    owner=models.ForeignKey('auth.User',related_name='albums',default=1)
    artist=models.CharField(max_length=250)
    album_title=models.CharField(max_length=500)
    genre=models.CharField(max_length=250)
    album_logo=models.FileField()

    #to redirect user to detail page after registration
    def get_absolute_url(self):
        return  reverse('music:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.album_title+"- "+self.artist



class Songs(models.Model):

    album=models.ForeignKey(Album,on_delete=models.CASCADE,related_name='songs')
    file_type=models.CharField(max_length=10)
    song_title=models.CharField(max_length=250)
    release_date=models.DateField()
    is_fav=models.BooleanField(default=False)
    music_file=models.FileField(upload_to='')
    def __str__(self):
        return self.song_title
