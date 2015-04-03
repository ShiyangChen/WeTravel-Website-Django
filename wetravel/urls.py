from django.conf.urls import patterns, url

from wetravel import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.user_login, name='login'),
)
