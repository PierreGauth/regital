
 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from navigation.models import Personne

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
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
	return HttpResponseRedirect(next)
	
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')
	
@login_required(login_url='/login/')
def saisie(request, active_tab='Personne', alert='off', alert_type='success', alert_message="unknown"):

    personneForm =  render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/personne/', 'formset' : PersonneForm(), 
        'alert' : alert, 'alert_type' : alert_type, 'alert_message' : alert_message, 'date_picker_id_list' : ['dp1','dp2'],
        'specific_function' : u'''
              function recupInfo() { 
                var nom = document.getElementsByName("nom")[0].value;
                var prenom = document.getElementsByName("prenom")[0].value; 
                if (nom != "" && prenom != "") { 
                  $.get( "../saisie/info/personne/"+nom+"/"+prenom, function( data ) 
                      {
                          addToModal("La personne que vous etes en train d\'enter correspond-t-elle à l\'une de ces personne ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data);
                      });
                  toogleModal(); }
              }
              
              
              function parseInfo(id) {
                $.get( "../saisie/info/personne/"+id, function( data ) 
                {
                    var values = data.split(';');                   
                    setValue('titre',values[1]);                                      
                    setValue('prenom',values[2]);                                                        
                    setValue('nom',values[4]);                                     
                    //setValue('date_de_naissance',values[5]);                                     
                    //setValue('date_de_deces',values[6]);                                               
                    setValue('pseudonyme',values[7]);
                    if(values[8] == 'male') setValue('genre','M');
                    else if(values[8] == 'female') setValue('genre','F'); 
                    if(values[9] == 'French') setValue('nationalite', 'fr');
                    else if(values[9] == 'Italian') setValue('nationalite', 'it');
                    else if(values[9] == 'Deutsch') setValue('nationalite', 'de');
                    else if(values[9] == 'English') setValue('nationalite', 'en');
                    else setValue('nationalite', '-');
                    if (values[10] /= 'undefined') setValue('plus_dinfo', values[10]);
                    setValue('uri_cesar','http://cesar.org.uk/cesar2/people/people.php?fct=edit&person_UOID='+id);
                });
                toogleModal();
              }

              '''},
        context_instance=RequestContext(request))
        
    return render_to_response('tab_page.html', 
        {"title":"Saisie", "active":"saisie", "tab_list" : 
        {"Personne" : personneForm, "Soiree":soireeForm, "Piece":"123456789"}, "active_tab":active_tab}, 
        context_instance=RequestContext(request))

    
@login_required(login_url='/login/')
def creerPersonne(request):
    if request.POST:
        nom = request.POST.get('nom', 'none')
        prenom = request.POST.get('prenom', 'none')
        pseudonyme = request.POST.get('pseudonyme', 'none')
        uri_cesar = request.POST.get('uri_cesar', 'none')
        genre = request.POST.get('genre', 'none')
        nationalite = request.POST.get('nationalite', 'none')
        titre = request.POST.get('titre', 'none')
        date_de_naissance = request.POST.get('date_de_naissance', 'none')
        date_de_deces = request.POST.get('date_de_deces', 'none')
        plus_dinfo = request.POST.get('plus_dinfo', 'none')
        personne = Personne(nom=nom, prenom=prenom, pseudonyme=pseudonyme, uri_cesar=uri_cesar, genre=genre, 
            nationalite=nationalite, titre=titre, date_de_naissance=date_de_naissance, 
            date_de_deces=date_de_deces, plus_dinfo=plus_dinfo)
        personne.save()
        message = u"<b>" + prenom + " " + nom + u"</b> a bien été ajouté dans la base"
	return saisie(request, active_tab='Personne',alert='on',alert_type='success',alert_message=message)
	  
def listPersonnes(request):
    personnes = Personne.objects.all()
    personnes_nom = {}
    
    for personne in personnes:
      print personne.nom
      personnes_nom[personne.id] = personne.nom
      
    return render_to_response('list_page.html',
      {'title':'Personnes', 'active':'personnes', 'list':personnes_nom, 'link':'/personnes/'},
      context_instance=RequestContext(request))
