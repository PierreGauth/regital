from django.conf.urls import patterns, url
from saisie import views, cesar, theaville

urlpatterns = patterns('',
  # .../saisie/
  url(r'^$', views.saisie),  
  url(r'^info/personne/(?P<nom>\w+)/(?P<prenom>\w+)$', cesar.searchPersonne),
  url(r'^info/piece/(?P<titre>\w+)$', theaville.searchPiece),
  url(r'^info/personne/(?P<id>\d+)$', cesar.getInfoPersonne),
  url(r'^new/personne/$', views.creerPersonne),
  url(r'^new/piece/$', views.creerPersonne),
  url(r'^new/soiree/$', views.creerSoiree),
	)
