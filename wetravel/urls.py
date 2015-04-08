from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wetravel import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^friends/', views.friends, name='friends'),
    url(r'^send_friend_request/', views.send_friend_request, name='send_friend_request'),
    url(r'^requests/', views.requests, name='requests')
)

urlpatterns += staticfiles_urlpatterns()