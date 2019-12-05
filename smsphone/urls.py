
from django.contrib import admin
from django.urls import path,include
from duanxin import views
urlpatterns = [
    path('', include("duanxin.urls")),
    path('captcha', include('captcha.urls')),
]
