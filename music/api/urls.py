from django.conf.urls import url
from .views import (
	AlbumListAPIView,
	AlbumDetailAPIView,
	SongListAPIView,
	SongDetailAPIView
	)


urlpatterns = [
    
     url(r'^$',AlbumListAPIView.as_view(),name="album-list"),
     url(r'^(?P<pk>[0-9]+)/$', AlbumDetailAPIView.as_view(),name='album-detail'),
     url(r'^songs/$',SongListAPIView.as_view(),name="songs-list"),
     url(r'^songs/(?P<pk>[0-9]+)/$', SongDetailAPIView.as_view(),name='song-detail'),
]