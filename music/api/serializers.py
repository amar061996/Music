from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	)
from music.models import Album,Songs

#User Model
from django.contrib.auth.models import User


album_detail_url=HyperlinkedIdentityField(
	view_name='music-api:detail',
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
		'album_title',



		]

class AlbumDetailSerializer(ModelSerializer):
	owner=UserDetailSerializer(read_only=True)

	class Meta:
		model=Album
		fields=[
		'album_title',
		'artist',
		'genre',
		'owner'

		]		