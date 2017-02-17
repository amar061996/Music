from .serializers import (
	AlbumListSerializer,
	AlbumDetailSerializer,
	SongListSerializer,
	SongDetailSerializer,
	)
#generic views
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)
#rest framework inbuilt filters
from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,


	)
from music.models import Album,Songs

class AlbumListAPIView(ListAPIView):
	queryset=Album.objects.all()
	serializer_class=AlbumListSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields=['album_title','artist','genre']


class AlbumDetailAPIView(RetrieveAPIView):
	queryset=Album.objects.all()
	serializer_class=AlbumDetailSerializer

class SongListAPIView(ListAPIView):
	queryset=Songs.objects.all()
	serializer_class=SongListSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields=['song_title']

class SongDetailAPIView(RetrieveAPIView):
	queryset=Songs.objects.all()
	serializer_class=SongDetailSerializer	