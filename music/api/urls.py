from django.conf.urls import url
from .views import AlbumListAPIView,AlbumDetailAPIView


urlpatterns = [
    
     url(r'^$',AlbumListAPIView.as_view(),name="album-api"),
     url(r'^(?P<pk>[0-9]+)/$', AlbumDetailAPIView.as_view(),name='detail'),
     

]