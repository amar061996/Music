from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)
from music.models import Album,Songs

#User Model
from django.contrib.auth.models import User


album_detail_url=HyperlinkedIdentityField(
	view_name='music-api:album-detail',
	lookup_field='pk'
	)
song_detail_url=HyperlinkedIdentityField(
	view_name='music-api:song-detail',
	lookup_field='pk'
	)

class UserDetailSerializer(ModelSerializer):
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'first_name',
			'last_name',

		]

class AlbumListSerializer(ModelSerializer):
	url=album_detail_url
	class Meta:
		model=Album
		fields=[
		'url',
		'id',
		'album_title',



		]

class AlbumDetailSerializer(ModelSerializer):
	owner=UserDetailSerializer(read_only=True)
	songs=SerializerMethodField()
	class Meta:
		model=Album
		fields=[
		'album_title',
		'artist',
		'genre',
		'owner',
		'songs',

		]

	def get_songs(self,obj):
		songs_qs=Songs.objects.filter(album=obj)
		songs=SongSerializer(songs_qs,many=True).data
		return songs			

class SongListSerializer(ModelSerializer):
	url=song_detail_url
	class Meta:
		model=Songs
		fields=[
		'url',
		'id',
		'song_title',
	

		]

class SongDetailSerializer(ModelSerializer):
	album=AlbumListSerializer()
	class Meta:
		model=Songs
		fields=[
		'album',
		'song_title',
		'file_type',
		'release_date'

		]		

class SongSerializer(ModelSerializer):

	class Meta:
		model=Songs
		fields=[
			'song_title',
			'file_type',
			'release_date',
		]		