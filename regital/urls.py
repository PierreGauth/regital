from django.conf.urls import patterns, include, url

from django.contrib import admin
from navigation import views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
  url(r'^login/', views.log_in, name='login'),
	url(r'^logout/', views.log_out, name='logout'), 
	# url(r'^pieces/', views.listPieces, name='pieces'),
	url(r'^personnes/', views.listPersonnes, name='personnes'),
	# url(r'^soirees/', views.listSoirees, name='soirees'),
	url(r'^saisie/$', views.saisie, name='saisie'),
  url(r'^saisie/new/personne/$', views.creerPersonne, name='creerPersonne'),
  url(r'^saisie/new/piece/$', views.creerPersonne, name='creerPiece'),
  url(r'^saisie/new/soiree/$', views.creerPersonne, name='creerSoiree'),
	url(r'^$', views.index, name='index'),
)
