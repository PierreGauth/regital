from django.conf.urls import patterns, url

from saisie import views

urlpatterns = patterns('',
	# .../saisie/
	url(r'^$', views.index, name='index'),
	# .../saisie/login/
	url(r'login/$', views.login_saisie, name='login_saisie'),
	# .../saisie/logout/
	url(r'logout/$', views.logout_saisie, name='logout_saisie'),
	)
