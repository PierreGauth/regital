from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^dataManager/', include('dataManager.urls', namespace="dataManager")),
    url(r'^saisie/', include('saisie.urls', namespace="saisie")),
    url(r'^admin/', include(admin.site.urls)),
)
