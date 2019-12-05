
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'duanxin'
urlpatterns = [
    path('', views.index,name='index'),
    path('redis/',views.test_redis,name="redis"),
    path('send_sms/',views.send_sms,name="send_sms"),
    path('check_sms/',views.check_sms,name="check_sms"),
    path("img_refresh/",views.img_refresh,name='img_refresh'),
    path("img_check",views.img_check,name="img_check"),
    path('ajax/',views.ajax,name='ajax'),
    path('ajax_html/',views.ajax_html,name='ajax_html'),
    path('login/',views.login,name='login'),
    path('books/',views.books,name='books'),
    path('booktype/',views.booktype,name='booktype'),
    path('booklink/<id>',views.booklink,name='booklink')
]

