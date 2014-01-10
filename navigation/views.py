from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from navigation.models import Personne, PersonneForm

def index(request):
    return render_to_response('accueil.html', {"active":"accueil"}, context_instance=RequestContext(request))

def log_in(request, next='/'):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST.get('username', 'none')
		password = request.POST.get('password', 'none')
		next = request.POST.get('next', 'none')
		next = next[next.index('//')+2:]
		next = next[next.index('/'):]
		print next
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
	return HttpResponseRedirect(next)
	
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')
	
@login_required(login_url='/login/')
def saisie(request):
    personneForm = PersonneForm()
    return render_to_response('tab_page.html', {"title":"Saisie", "active":"saisie", "tab_list" : {"Personne" : personneForm, "Soiree":"azertyu", "Piece":"123456789"}, "activate":"Personne"}, context_instance=RequestContext(request))