"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from songs import views
from django.conf import settings
from django.conf.urls.static import static
import urllib.parse
from api.views import MusicListView,MusicDateAPIView,ArtistListAPIView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'home' ),
    path('api/', MusicListView.as_view()),
    path('api/date/', MusicDateAPIView.as_view()),
    path('api/singer/', ArtistListAPIView.as_view()),
    # path('rev/<str:song>/<str:artist>/',views.rev, name = 'rev'),
    path('result/<str:song>/<str:artist>/',views.result, name = 'result'),
]


 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
