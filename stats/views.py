 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from navigation.models import *

	
def statsForm(request):

	return render_to_response('stats.html', 
		{"title":"Statistiques", "active":"statistiques"}, 
		context_instance=RequestContext(request))