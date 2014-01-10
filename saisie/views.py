from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/login/')
def index(request):
    return render_to_response('saisie/saisie.html', {'connected': True}, context_instance=RequestContext(request))

def login_saisie(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST.get('username', 'none')
		password = request.POST.get('password', 'none')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/saisie/')
	return render_to_response('saisie/login.html', {'wanted_page' : 'saisie/saisie.html'}, context_instance=RequestContext(request))
	
def logout_saisie(request):
	logout(request)
	return HttpResponseRedirect('/saisie/')