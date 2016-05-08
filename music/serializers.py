from rest_framework import serializers
from .models import Album,Songs
from django.contrib.auth.models import User




class SongsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Songs
        fields=('song_title','file_type',)



class AlbumSerializer(serializers.ModelSerializer):

    owner=serializers.ReadOnlyField(source='owner.username')
    songs=SongsSerializer(many=True)
    class Meta:
       model=Album
       fields=('id','artist','album_title','genre','album_logo','owner','songs')


class UserSerializer(serializers.ModelSerializer):

    albums=AlbumSerializer(many=True)

    class Meta:
        model=User
        fields=('id','username','albums')



