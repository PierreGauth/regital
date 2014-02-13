 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from navigation.models import Personne,Piece,Soiree,BudgetSoiree
from saisie.forms import *

	
@login_required(login_url='/login/')
def saisie(request, active_tab='Soiree', alert='off', alert_type='success', alert_message="unknown", previous_values = {}):

    personneForm = render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/personne/', 'formset_list' : [PersonneForm()],'date_picker_id_list' : ['dpersonne1','dpersonne2'], 
        'previous_values' : previous_values, 'specific_function' : getPersonneJs()},
        context_instance=RequestContext(request)) + render_to_string(
        'modal.html' , 
        {'modalId' : 'personneModal', 'modalTitle' : 'Recherche sur Cesar'},
        context_instance=RequestContext(request))
    
    pieceForm = render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/piece/', 'formset_list' : [PieceForm()], 'date_picker_id_list' : ['dpiece1'],
        'previous_values' : previous_values, 'specific_function' : getPieceJs()},
        context_instance=RequestContext(request))
        
    soireeForm = render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/soiree/', 'formset_list' : [SoireeForm(), BudgetSoireeForm()], 
        'previous_values' : previous_values, 'date_picker_id_list' : ['dsoiree1']},
        context_instance=RequestContext(request))
        
    return render_to_response('tab_page.html', 
        {"title":"Saisie", "active":"saisie", "tab_list" : 
        {"Personne" : personneForm, "Soiree":soireeForm, "Piece":pieceForm}, "active_tab":active_tab,  
        'alert' : alert, 'alert_type' : alert_type, 'alert_message' : alert_message}, 
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
        try:
          personne.save()
          message = u"<b>" + prenom + " " + nom + u"</b> a bien été ajouté dans la base"
          return saisie(request, active_tab='Personne',alert='on',alert_type='success',alert_message=message)
        except ValidationError as e:
          message = ' '.join(e.messages)
          return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'nom':nom,
                      'prenom':prenom,
                      'pseudonyme':pseudonyme,
                      'uri_cesar':uri_cesar,
                      'genre':genre,
                      'nationalite':nationalite,
                      'titre':titre,
                      'date_de_naissance':date_de_naissance,
                      'date_de_deces':date_de_deces,
                      'plus_dinfo' : plus_dinfo})
        except IntegrityError as e:
          message = 'Cette Personne existe déja dans la base'
          return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'nom':nom,
                      'prenom':prenom,
                      'pseudonyme':pseudonyme,
                      'uri_cesar':uri_cesar,
                      'genre':genre,
                      'nationalite':nationalite,
                      'titre':titre,
                      'date_de_naissance':date_de_naissance,
                      'date_de_deces':date_de_deces,
                      'plus_dinfo' : plus_dinfo}) 
                      
@login_required(login_url='/login/')
def creerPiece(request):
    if request.POST:
        titre = request.POST.get('titre', 'none')
        titre_brenner = request.POST.get('titre_brenner', 'none')
        uri_theaville = request.POST.get('uri_theaville', 'none')
        date_premiere = request.POST.get('date_premiere', 'none')
        langue = request.POST.get('langue', 'none')
        auteurs = request.POST.get('auteurs', 'none')
        commentaire = request.POST.get('commentaire', 'none')
        
        piece = Piece(titre=titre, titre_brenner=titre_brenner, uri_theaville=uri_theaville, date_premiere=date_premiere, langue=langue, commentaire=commentaire)
        
        try:
          piece.save()
          piece.auteurs.add(auteurs)
          message = u"<b>" + titre + u"</b> a bien été ajouté dans la base"
          return saisie(request, active_tab='Piece',alert='on',alert_type='success',alert_message=message)
        except ValidationError as e:
          message = ' '.join(e.messages)
          return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'titre':titre,
                      'titre_brenner':titre_brenner,
                      'date_premiere':date_premiere,
                      'uri_theaville':uri_theaville,
                      'langue':langue,
                      'auteurs':auteurs,
                      'commentaire':commentaire})
        except IntegrityError as e:
          message = 'Cette Piece existe déja dans la base'
          return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'titre':titre,
                      'titre_brenner':titre_brenner,
                      'date_premiere':date_premiere,
                      'uri_theaville':uri_theaville,
                      'langue':langue,
                      'auteurs':auteurs,
                      'commentaire':commentaire})
        

@login_required(login_url='/login/')
def creerSoiree(request):
    if request.POST:
        date = request.POST.get('date', 'none')
        libelle_date_reg = request.POST.get('libelle_date_reg', 'none')
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
        message = u"<b>La soiree du " + date + "u (" + nom + u")</b> a bien été ajouté dans la base"
	return saisie(request, active_tab='Personne',alert='on',alert_type='success',alert_message=message)
  
def getPersonneJs():
  return '''
function recupPersonneInfo() { 
  var nom = document.getElementsByName("nom")[0].value;
  var prenom = document.getElementsByName("prenom")[0].value; 
  if (nom != "" && prenom != "") { 
    $.get( "../saisie/info/personne/"+nom+"/"+prenom, function( data ) 
        {
          addTopersonneModal("La personne que vous etes en train d\'enter correspond-t-elle à l\'une de ces personnes ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data);
        });
        tooglepersonneModal();
     }
}              

function parsePersonneInfo(id) {
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
  tooglepersonneModal();
}'''

def getPieceJs():
  return '''
function recupPieceInfo() { 

}              

function parsePieceInfo(id) {
  $.get( "../saisie/info/personne/"+id, function( data ) 
  {
  });
}'''