"""raspi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from live.views import livefe,streaming,login,main_loged_in,savedimg,dbserial,myserial,videourl,urlget,gall

urlpatterns = [
    path('admin/', admin.site.urls),
    path('video_feed/', livefe,name='video_feed'),
    path('streaming/',streaming),
    path('accounts/',include('allauth.urls')),
    path('streaming/<int:imgNum>/',savedimg),
    path('',login),
    path('main_loged_in/',main_loged_in),
    path('serial',dbserial),
    path('myserial',myserial),
    path('youtube/<str:url>',videourl),
    path('urlget/',urlget),
    path('gall/',gall),

]
