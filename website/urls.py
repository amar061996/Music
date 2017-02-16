
from django.conf.urls import url,include
from django.contrib import admin
from music import views
from django.conf.urls.static import static
from django.conf import  settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home,name='home'),
    url(r'^music/', include('music.urls')),
]

urlpatterns += [
    url(r'^api/music/',include("music.api.urls", namespace="music-api")),
]

if settings.DEBUG:
     urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
     urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)