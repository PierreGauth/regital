from django.conf.urls import patterns, url

from saisie import views

urlpatterns = patterns('',
	# .../saisie/
	url(r'^$', views.index, name='index'),
	# .../saisie/login/
	url(r'login/$', views.login, name='login'),
	)
