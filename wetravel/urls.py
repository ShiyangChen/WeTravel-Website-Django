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
    url(r'^process_request/', views.process_request, name='process_request'),
    url(r'^places/', views.places, name='places'),
    url(r'^add_to_visit',views.add_to_visit, name='add_to_visit'),
    url(r'^add_visited',views.add_visited, name='add_visited'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^create-post/$', views.createpost, name='create_post'),
    url(r'^createpost/$', views.createpost, name='createpost'),
    url(r'^profile/(\d+)/$',views.profile, name='profile'),
    url(r'^delete_confirm/(\d+)/$',views.delete_confirm),
    url(r'^delete/(\d+)/$',views.delete),
    url(r'^privacy_choose/(\d+)/$',views.privacy_choose),
    url(r'^privacy/(\d+)/$',views.privacy),
    url(r'^change_address/$', views.change_address, name='change_address'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^change_profile_image/$', views.change_profile_image, name='change_profile_image'),
    url(r'^comment_upload/(\d+)/$',views.comment_upload,name='comment_upload'),
    url(r'^schedule/$', views.schedule),
    url(r'^schedule_edit/(?P<travel_id>[0-9]+)/$', views.schedule_edit)

)

urlpatterns += staticfiles_urlpatterns()
