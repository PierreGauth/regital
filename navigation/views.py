
 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.db.models import Q
from navigation.models import *

def index(request):
	return render_to_response('accueil.html', {"title":"Accueil", "active":"accueil"}, context_instance=RequestContext(request))
	
	

def test_chart(request):

	data = [
	{'x' : 'date', 'y' : 'nbSpectateur', 'opt' : ['langue', 'partie']},
	{'date': '1702-02-05', 'nbSpectateur' : 1234, 'langue' : 'f', 'partie' : '1'},
	{'date': '1702-02-09', 'nbSpectateur' : 3234, 'langue' : 'f', 'partie' : '1'},
	{'date': '1702-02-22', 'nbSpectateur' : 2234, 'langue' : 'f', 'partie' : '1'},
	{'date': '1702-03-05', 'nbSpectateur' : 1294, 'langue' : 'i', 'partie' : '1'},
	{'date': '1703-03-05', 'nbSpectateur' : 1236, 'langue' : 'f', 'partie' : '2'},
	{'date': '1703-07-05', 'nbSpectateur' : 1534, 'langue' : 'f', 'partie' : '1'},
	{'date': '1703-09-05', 'nbSpectateur' : 2234, 'langue' : 'i', 'partie' : '2'},
	{'date': '1703-09-05', 'nbSpectateur' : 2234, 'langue' : 'f', 'partie' : '2'},
	{'date': '1703-10-05', 'nbSpectateur' : 234, 'langue' : 'f', 'partie' : '1'},
	{'date': '1703-12-05', 'nbSpectateur' : 34, 'langue' : 'f', 'partie' : '2'},
	{'date': '1704-02-05', 'nbSpectateur' : 6234, 'langue' : 'i', 'partie' : '2'},
	{'date': '1704-03-05', 'nbSpectateur' : 4214, 'langue' : 'f', 'partie' : '2'},
	{'date': '1705-04-05', 'nbSpectateur' : 2234, 'langue' : 'f', 'partie' : '2'},
	{'date': '1705-05-05', 'nbSpectateur' : 1834, 'langue' : 'i', 'partie' : '1'},
	{'date': '1705-06-05', 'nbSpectateur' : 1934, 'langue' : 'i', 'partie' : '1'},
	{'date': '1708-02-05', 'nbSpectateur' : 934, 'langue' : 'i', 'partie' : '2'},
	{'date': '1708-08-05', 'nbSpectateur' : 734, 'langue' : 'f', 'partie' : '1'},
	{'date': '1708-09-05', 'nbSpectateur' : 234, 'langue' : 'i', 'partie' : '1'},
	{'date': '1708-10-05', 'nbSpectateur' : 1244, 'langue' : 'i', 'partie' : '1'},
	{'date': '1710-02-05', 'nbSpectateur' : 2234, 'langue' : 'f', 'partie' : '1'},
	{'date': '1710-05-05', 'nbSpectateur' : 3254, 'langue' : 'f', 'partie' : '2'},
	{'date': '1712-02-05', 'nbSpectateur' : 6214, 'langue' : 'i', 'partie' : '1'},
	{'date': '1736-02-05', 'nbSpectateur' : 4294, 'langue' : 'i', 'partie' : '2'},
	{'date': '1786-02-05', 'nbSpectateur' : 2274, 'langue' : 'i', 'partie' : '2'}
	]

	return render_to_response('chart/test_chart.html', {'data1':data},	context_instance=RequestContext(request))	
	
	

def log_in(request, next='/'):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST.get('username', 'none')
		password = request.POST.get('password', 'none')
		next = request.POST.get('next', 'none')
		next = next[next.index('//')+2:]
		next = next[next.index('/'):]
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
	return HttpResponseRedirect(next)
	
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')
	  
def listPersonnes(request):

	if request.POST: #Pour le trie par ordre alphabétique et la pagination
		startwith = request.POST.get('start_with', '')
		page = int(request.POST.get('page_num', '1'))
	else :
		startwith = ''
		page = 1
		
	personnes = Personne.objects.all().filter(Q(nom__startswith=startwith) | Q(prenom__startswith=startwith)).order_by('nom','prenom')  
	page_nb = len(personnes)/20 + 1
	personnes = personnes[20*(page-1):20*page]
  
	personnes_nom = [(personne.id, personne.titre_personne+" "+personne.nom+" "+personne.prenom) for personne in personnes]
					    
	return render_to_response('list_page.html',
		{'title':'Personnes', 'active':'personnes', 'list':personnes_nom, 'link':'/personnes/', 
		'page_nb': page_nb, 'start_with': startwith, 'page_num': page },
		context_instance=RequestContext(request))

def listPieces(request):

	if request.POST: #Pour le trie par ordre alphabétique et la pagination
		startwith = request.POST.get('start_with', '')
		page = int(request.POST.get('page_num', '1'))
	else :
		startwith = ''
		page = 1

	pieces = Piece.objects.all().filter(titre__startswith=startwith).order_by('titre')  
	page_nb = len(pieces)/20 + 1
	pieces = pieces[20*(page-1):20*page]

	piece_titre = [(piece.id, piece.titre) for piece in pieces]

	return render_to_response('list_page.html',
	{'title':'Pieces', 'active':'pieces', 'list':piece_titre, 'link':'/pieces/', 
	'page_nb': page_nb, 'start_with': startwith, 'page_num': page },
	context_instance=RequestContext(request))
      
def listSoirees(request,date='1700-01-01'):

 	soirees = Soiree.objects.all()
	soireesVide = SoireeVide.objects.all()
	soiree_date = []

	for soiree in soirees:
		soiree_date.append({'Date' : str(soiree.date), 'Exist' : '1'})
	for soireeVide in soireesVide:
		soiree_date.append({'Date' : str(soireeVide.date), 'Exist' : '-1'})
	
	return render_to_response('list_soiree.html',
	{'title':'Soirees', 'active':'soirees', 'list_soirees':soiree_date, 'date':date, 'link':'/soirees/'},
	context_instance=RequestContext(request))
	
def detailsPersonne(request,id):
  personne=Personne.objects.get(id=id)
  personne_nationalite=personne.get_nationalite_display()
  personne_genre=personne.get_genre_display()
  return render_to_response('page_detail_personne.html',
    {'title':personne.prenom+' '+personne.nom,
    'active':'personnes',
    'personneinfos':personne,
    'personne_nationalite':personne_nationalite,
    'personne_genre':personne_genre},
    context_instance=RequestContext(request))

def detailsPiece(request,id):
  piece=Piece.objects.get(id=id)
  piece_langue=piece.get_langue_display()
  return render_to_response('page_detail_piece.html',
    {'title':piece.titre,
    'active':'pieces',
    'pieceinfos':piece,
    'piece_langue':piece_langue,},
    context_instance=RequestContext(request))

def detailsSoiree(request,date):
	try :
		soiree = Soiree.objects.get(date = date)
		billetteries = Billetterie.objects.all().filter(budget = soiree.budget)
		debits = Debit.objects.all().filter(budget = soiree.budget)
		credits = Credit.objects.all().filter(budget = soiree.budget).exclude(id__in=billetteries)
		liste_representations = []
		representations = Representation.objects.all().filter(Soiree = soiree)
		animations = Animation.objects.all().filter(Soiree = soiree)
		for rep in representations : 
			liste_representations.append(rep)
		for rep in animations : 
			liste_representations.append(rep)
	except ObjectDoesNotExist as e:
		return listSoirees(request,date)
	return render_to_response('page_detail_soiree.html',
    {'title':str(soiree.date),
    'active':'soirees',
    'soireeinfos':soiree,
		'billetterieinfos':billetteries,
		'debitsinfos':debits,
		'creditsinfos':credits,
		'liste_representations': liste_representations},
    context_instance=RequestContext(request))

