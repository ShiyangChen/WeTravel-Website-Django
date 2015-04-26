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
    url(r'^requests/', views.requests, name='requests'),
    url(r'^addplace/', views.add_place, name='addplace'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^create-post/$', views.create_post),
    url(r'^createpost/$', views.createpost),
    url(r'^profile/$',views.profile),
    url(r'^delete_confirm/(\d+)/$',views.delete_confirm),
    url(r'^delete/(\d+)/$',views.delete),
    url(r'^privacy_choose/(\d+)/$',views.privacy_choose),
    url(r'^privacy/(\d+)/$',views.privacy),
)

urlpatterns += staticfiles_urlpatterns()
