"""
URL configuration for godwish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

app_name = 'elements'

urlpatterns = [
    # path('up',views.up,name='up'),
    path('up', views.PictureWorkView.as_view(), name='up'),
    path('galery_pic', views.GaleryView.as_view(), name='galery_pic'),
    path('up_docs', views.DocumentUpload.as_view(), name='up_docs'),
    path('doclist', views.DocList.as_view(), name='doclist'),
    path('upItem', views.CompCreate.as_view(), name='upItem'),
    path('showItem', views.CompShow.as_view(), name='showItem'),

]
