from django.conf.urls import patterns, include, url

from django.contrib import admin
from navigation import views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
    url(r'login/', views.log_in, name='login'),
	url(r'logout/', views.log_out, name='logout'),
	url(r'saisie/', views.saisie, name='saisie'),
	url(r'^$', views.index, name='index'),
)
