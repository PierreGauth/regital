from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

def index(request):
    return render_to_response('saisie/login.html', {}, context_instance=RequestContext(request))

def login(request):
    return render_to_response('saisie/login.html', {}, context_instance=RequestContext(request))
