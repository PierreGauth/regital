from django.conf.urls import patterns, include, url

from django.contrib import admin
from navigation import views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
  url(r'^login/', views.log_in),
	url(r'^logout/', views.log_out), 
	url(r'^pieces/$', views.listPieces),
	url(r'^pieces/(?P<id>\d+)$', views.detailsPiece),
	url(r'^personnes/$', views.listPersonnes),
	url(r'^personnes/(?P<id>\d+)$', views.detailsPersonne),
	url(r'^soirees/', views.listSoirees),
	url(r'^saisie/', include('saisie.urls')),
	url(r'^$', views.index),
)
