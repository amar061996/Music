from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

from django.contrib.auth.decorators import login_required

app_name='music'


urlpatterns = [
    #api
     url(r'^api/users$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api/$', views.AlbumList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$',views.AlbumDetail.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$',views.AlbumDetail.as_view()),

    #tutorial

    url(r'^$', views.IndexView.as_view(),name='index'),
    #register
     url(r'^register/$', views.UserFormView.as_view(),name='register'),
    #login
    url(r'^login/$', views.LoginFormView.as_view(),name='login'),
    #logout
    url(r'^logout/$', views.logoutUser,name='logout'),
    #details
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(),name='detail'),
    #music/1/add_songs
    url(r'^(?P<album_id>[0-9]+)/add_songs/$', views.SongsView.as_view(),name='add_songs'),#add songs to album
    #music/1/delete_song/2
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)$', views.songDelete,name='delete_song'), #delete song
    url(r'^(?P<album_id>[0-9]+)/play_song/(?P<song_id>[0-9]+)$', views.playSong,name='play'),
    #music/album/add
    url(r'^album/add$',login_required(views.AlbumCreate.as_view()),name='album_add'),  #create
    #music/album/2/update
    url(r'^album/(?P<pk>[0-9]+)/update$', login_required(views.AlbumUpdate.as_view())   ,name='album_update'), #update
    #music/album/2/delete
    url(r'^album/(?P<pk>[0-9]+)/delete$', login_required(views.AlbumDelete.as_view()),name='album_delete'), #delete
    

]

urlpatterns = format_suffix_patterns(urlpatterns)

#for favorite
#  url(r'^(?P<album_id>[0-9]+)/favorite$', views.favorite,name='favorite'),


#for function based view
"""
    url(r'^$', views.index,name='index'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail,name='detail'),

"""