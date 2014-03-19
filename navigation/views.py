
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
from navigation.models import *

def index(request):
	return render_to_response('accueil.html', {"title":"Accueil", "active":"accueil"}, context_instance=RequestContext(request))

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
    personnes = Personne.objects.all()
    personnes_nom = {}
    
    for personne in personnes:
      print personne.nom
      personnes_nom[personne.id] = personne.nom+" "+personne.prenom
      
    return render_to_response('list_page.html',
      {'title':'Personnes', 'active':'personnes', 'list':personnes_nom, 'link':'/personnes/'},
      context_instance=RequestContext(request))

def listPieces(request):
  if request.POST:
    search = request.POST.get('search', '')
    pieces = Piece.objects.all().filter(titre__contains=search)
  else:
    pieces = Piece.objects.all()
    
  pieces_titre = {}
  
  for piece in pieces:
    pieces_titre[piece.id] = piece.titre
    
  return render_to_response('list_page.html',
    {'title':'Pieces', 'active':'pieces', 'list':pieces_titre, 'link':'/pieces/'},
    context_instance=RequestContext(request))
      
def listSoirees(request,date='1700-01-01'):
	if request.POST:
		year = request.POST.get('year', '')
		month = request.POST.get('month', '')
		day = request.POST.get('day', '')
		if year != '':
			if month != '':
				if day != '':
					soirees = Soiree.objects.all().filter(date__year = year, date__month = month, date__day = day)
				else:
					soirees = Soiree.objects.all().filter(date__year = year, date__month = month)
			else:
				if day != '':
					soirees = Soiree.objects.all().filter(date__year = year, date__day = day)
				else:
					soirees = Soiree.objects.all().filter(date__year = year)
		else:
			if month != '':
				if day != '':
					soirees = Soiree.objects.all().filter(date__month = month, date__day = day)
				else:
					soirees = Soiree.objects.all().filter(date__month = month)
			else:
				if day != '':
					soirees = Soiree.objects.all().filter(date__day = day)
				else:
					soirees = Soiree.objects.all()

	else:
		soirees = Soiree.objects.all()

	soiree_date = []

	for soiree in soirees:
		soiree_date.append({'Date' : str(soiree.date), 'Exist' : '1'})
	
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

