 #-*- coding: utf-8 -*-
 
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db import IntegrityError
from navigation.models import *
from saisie.forms import *
import re, ast

	
@login_required(login_url='/login/')
def saisie(request, active_tab='Soiree', alert='off', alert_type='success', alert_message="unknown", previous_values = {}, date=''):

	# Quand on click sur une case vide du calendrier
	previous_values['date'] = date

	personneForm = render_to_string(
		'form.html' , 
		{'action' : '/saisie/new/personne/', 'formset_list' : {'PersonneForm':PersonneForm()},
		'date_picker_id_list' : ['dpersonne1','dpersonne2'], 'previous_values' : previous_values, 
		'specific_function' : 'saisie_personne.js', 'alertZoneId':'azpersonne', 'formId':'personneForm'},
		context_instance=RequestContext(request)) + render_to_string(
		'modal.html' , 
		{'modalId' : 'personneModal', 'modalTitle' : 'Recherche sur Cesar'},
		context_instance=RequestContext(request))

	pieceForm = render_to_string(
		'form.html' , 
		{'action' : '/saisie/new/piece/', 'formset_list' : {'PieceForm':PieceForm()}, 
		'date_picker_id_list' : ['dpiece1'],b'previous_values' : previous_values, 
		'specific_function' : 'saisie_piece.js', 'alertZoneId':'azpiece', 'formId':'pieceForm'},
		context_instance=RequestContext(request)) + render_to_string(
		'modal.html' , 
		{'modalId' : 'pieceModal', 'modalTitle' : 'Recherche sur Theaville'},
		context_instance=RequestContext(request))

	soireeForm = render_to_string(
		'form_soiree.html' , 
		{'action' : '/saisie/new/soiree/', 
		'formset_list' : { 'PageRegistreForm' : PageRegistreForm(), 'SoireeForm' : SoireeForm(), 'BudgetSoireeForm' : BudgetSoireeForm()}, 
		'formitems' : {'representation': RepresentationForm, 'animation': AnimationForm() ,'debit':DebitForm(),
		'credit':CreditForm(),'billetterie':BilletterieForm()}, 'formId' : 'soireeForm',
		'previous_values' : previous_values, 'specific_function' : 'saisie_soiree.js', 'date_picker_id_list' : ['dsoiree1']},
		context_instance=RequestContext(request))

	return render_to_response('tab_page.html', 
		{"title":"Saisie", "active":"saisie", "tab_list" : 
		{"Personne" : personneForm, "Soiree":soireeForm, "Piece":pieceForm}, "active_tab":active_tab, 
		'alert' : alert, 'alert_type' : alert_type, 'alert_message' : alert_message}, 
		context_instance=RequestContext(request))
				

@login_required(login_url='/login/')
def creerPersonne(request):
	if request.POST:		
		data = { x:y for x,y in request.POST.iteritems() }
		data = testDateForm(data,['date_de_naissance','date_de_deces'])	
		
		# Info concernant la piece ou la soirée depuis laquele la personne à été créée
		data['other_information'] = data['other_information'].replace('&', '","')
		data['other_information'] = data['other_information'].replace('=', '":"')		
		data['other_information'] = data['other_information'].replace('+', ' ')
		if data['other_information']=='':
			goBackTo = 'Personne'
			prevData = {}
		else :
			goBackTo = 'Soiree'
			prevData = ast.literal_eval('{"' + data['other_information'] + '"}')
		del data['other_information']
	
		personne = PersonneForm(data)
		
		try:
			instance = personne.save()
			message = u'<b><a href="/personnes/' + str(instance.id) + '">' + data['prenom'] + ' ' + data['nom'] + u'</a></b> a bien été ajouté dans la base'
			return saisie(request, active_tab=goBackTo,alert='on',alert_type='success',alert_message=message, previous_values = prevData)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
			  previous_values = request.POST)
		except ValueError as e:
			message = e
			return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
			  previous_values = request.POST)
		except IntegrityError as e:
			message = e
			return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
				previous_values = request.POST)
                      
@login_required(login_url='/login/')
def creerPiece(request):
	if request.POST:	
		data = { x:y for x,y in request.POST.iteritems() }
		data = testDateForm(data,['date_premiere'])	
		if 'auteurs' in data : del data['auteurs']
		
		# Info concernant la piece ou la soirée depuis laquele la personne à été créée
		data['other_information'] = data['other_information'].replace('&', '","')
		data['other_information'] = data['other_information'].replace('=', '":"')		
		data['other_information'] = data['other_information'].replace('+', ' ')
		if data['other_information']=='':
			goBackTo = 'Piece'
			prevData = {}
		else :
			goBackTo = 'Soiree'
			prevData = ast.literal_eval('{"' + data['other_information'] + '"}')
		del data['other_information']

		auteurs = [ Personne.objects.get(id=int(x)) for x in request.POST.getlist('auteurs')]
		piece = PieceForm(data)
		
		try:
			instance = piece.save()
			for auteur in auteurs : instance.auteurs.add(auteur)
			message = u'<b><a href="/pieces/' + str(instance.id) + '">' + instance.titre + u'</a></b> a bien été ajouté dans la base'
			return saisie(request, active_tab='Piece',alert='on',alert_type='success',alert_message=message)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
				previous_values = request.POST)
		except ValueError as e:
			message = e
			return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
			  previous_values = request.POST)
#		except IntegrityError as e:
#			message = 'Cette Piece existe déja dans la base'
#			return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
#				previous_values = request.POST)
        

@login_required(login_url='/login/')
def creerSoiree(request):
	if request.POST:
		try:
			ref_registre = request.POST.get('ref_registre', 'none')
			num_page_pdf = request.POST.get('num_page_pdf', 'none')
			redacteur = request.POST.get('redacteur', 'none')
			page_registre = PageRegistre(ref_registre=ref_registre, num_page_pdf=num_page_pdf)
			page_registre.save()

			total_depenses_reg = request.POST.get('total_depenses_reg', 'none')
			nb_total_billets_vendus_reg = request.POST.get('nb_total_billets_vendus_reg', 'none')
			total_recettes_reg = request.POST.get('total_recettes_reg', 'none')
			debit_derniere_soiree_reg = request.POST.get('debit_derniere_soiree_reg', 'none')
			total_depenses_corrige_reg = request.POST.get('total_depenses_corrige_reg', 'none')
			quart_pauvre_reg = request.POST.get('quart_pauvre_reg', 'none')
			debit_initial_reg = request.POST.get('debit_initial_reg', 'none')
			reste_reg = request.POST.get('reste_reg', 'none')
			nombre_cachets = request.POST.get('nombre_cachets', 'none')
			montant_cachet = request.POST.get('montant_cachet', 'none')
			montant_cachet_auteur = request.POST.get('montant_cachet_auteur', 'none')
			credit_final_reg = request.POST.get('credit_final_reg', 'none')
			budgetSoiree = BudgetSoiree(total_depenses_reg=total_depenses_reg, nb_total_billets_vendus_reg=nb_total_billets_vendus_reg, total_recettes_reg=total_recettes_reg, debit_derniere_soiree_reg=debit_derniere_soiree_reg, total_depenses_corrige_reg=total_depenses_corrige_reg, quart_pauvre_reg=quart_pauvre_reg, debit_initial_reg=debit_initial_reg, reste_reg=reste_reg, nombre_cachets=nombre_cachets, montant_cachet=montant_cachet, montant_cachet_auteur=montant_cachet_auteur, credit_final_reg=credit_final_reg)
			budgetSoiree.save()

			nb_debit = 0
			montant = request.POST.get('debit'+str(nb_debit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('debit'+str(nb_debit)+'libelle', 'none')
				type_depense = request.POST.get('debit'+str(nb_debit)+'type_depense', 'none')
				traduction = request.POST.get('debit'+str(nb_debit)+'traduction', 'none')
				mots_clefs = request.POST.get('debit'+str(nb_debit)+'mots_clefs', 'none')
				nb_debit += 1
				debit = Debit(montant=montant, libelle=libelle, type_depense=type_depense, traduction=traduction, mots_clefs=mots_clefs, budget=budgetSoiree)
				debit.save()
				montant = request.POST.get('debit'+str(nb_debit)+'montant', 'none')

			nb_credit = 0
			montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('credit'+str(nb_credit)+'libelle', 'none')
				nb_credit += 1
				credit = Credit(montant=montant, libelle=libelle, budget=budgetSoiree)
				credit.save()
				montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')

			nb_billetterie = 0
			montant = request.POST.get('billetterie'+str(nb_billetterie)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('billetterie'+str(nb_billetterie)+'libelle_debit', 'none')
				nombre_billets_vendus = request.POST.get('billetterie'+str(nb_billetterie)+'nombre_billets_vendus', 'none')
				type_billet = request.POST.get('billetterie'+str(nb_billetterie)+'type_billet', 'none')
				commentaire = request.POST.get('billetterie'+str(nb_billetterie)+'commentaire', 'none')
				nb_billetterie += 1
				billetterie = Billetterie(montant=montant, libelle=libelle, budget=budgetSoiree, nombre_billets_vendus=nombre_billets_vendus, type_billet=type_billet, commentaire=commentaire)
				billetterie.save()
				montant = request.POST.get('billetterie'+str(nb_billetterie)+'montant', 'none')

			date = request.POST.get('date', 'none')
			libelle_date_reg = request.POST.get('libelle_date_reg', 'none')
			ligne_src = request.POST.get('ligne_src', 'none') 
			soiree = Soiree(date=date, libelle_date_reg=libelle_date_reg, budget=budgetSoiree, ligne_src=ligne_src, page_registre=page_registre)
			soiree.save()
			
			nb_representations = 0
			position = request.POST.get('representation'+str(nb_representations)+'position', 'none')
			while position != 'none' :
				piece = request.POST.get('representation'+str(nb_representations)+'piece', 'none')
				nb_representations += 1
				representation = Representation(position=position, piece=Piece.objects.get(id=int(piece)), Soiree=soiree)
				representation.save()
				position = request.POST.get('representation'+str(nb_representations)+'position', 'none')
				
			nb_animations = 0
			position = request.POST.get('animation'+str(nb_animations)+'position', 'none')
			while position != 'none' :
				type = request.POST.get('animation'+str(nb_animations)+'type', 'none')
				auteur = request.POST.get('animation'+str(nb_animations)+'auteur', 'none')
				description = request.POST.get('animation'+str(nb_animations)+'description', 'none')
				nb_animations += 1
				animation = Animation(position=position, type=type, auteur=Personne.objects.get(id=int(auteur)), description=description, Soiree=soiree)
				animation.save()
				position = request.POST.get('animation'+str(nb_animations)+'position', 'none')
				
			message = u"La soirée du<a href='/soirees/"+soiree.date+"'><b> " + date + u"</a></b> a bien été ajouté dans la base"
			return saisie(request, active_tab='Soiree',alert='on',alert_type='success',alert_message=message)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message)
#		except IntegrityError as e:
#			message = 'Cette Soirée existe déja dans la base'
#			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message)


@login_required(login_url='/login/')
def update(request, type, id) :
	instance = {}
	if type == 'personne':
		instance = model_to_dict(Personne.objects.get(id=id))
	elif type == 'piece':
		instance = model_to_dict(Piece.objects.get(id=id))
	else :
		instance = model_to_dict(Soiree.objects.get(id=id))
	return saisie(request,active_tab=type.capitalize(), previous_values=instance)


# Permet la mise en forme des champs date listé (list_champs_date) dans un dictionnaire donné (data)	  
def testDateForm(data, list_champs_date) :
	for champs_date in list_champs_date:
		date = data[champs_date]
		data[champs_date+'_isComplete'] = True
		dateTextIsBlank = True
		if '?' in date:
			data[champs_date+'_text'] = date
			data[champs_date+'_isComplete'] = False
			dateTextIsBlank = False
			date = date.replace(u'?',u'0')
			date = date.replace(u'.',u'0')
		if re.match(r'^\d{4}$',date, re.UNICODE):
			if dateTextIsBlank :
				data[champs_date+'_text'] = date
				data[champs_date+'_isComplete'] = False
				dateTextIsBlank = False
			date += '-01-01'
			data[champs_date] = date
		if re.match(r'^[\w,û,é]* \d{4}$',date, re.UNICODE):
			if dateTextIsBlank :
				data[champs_date+'_text'] = date
				data[champs_date+'_isComplete'] = False
				dateTextIsBlank = False
			date = '01 '+date
		if re.match(r'^\d{1,2} [\w,û,é]* \d{4}$',date, re.UNICODE):
			date = date.replace(u'janvier',u'01')
			date = date.replace(u'février',u'02')
			date = date.replace(u'mars',u'03')
			date = date.replace(u'avril',u'04')
			date = date.replace(u'mai',u'05')
			date = date.replace(u'juin',u'06')
			date = date.replace(u'juillet',u'07')
			date = date.replace(u'août',u'08')
			date = date.replace(u'septembre',u'09')
			date = date.replace(u'octobre',u'10')
			date = date.replace(u'novembre',u'11')
			date = date.replace(u'décembre',u'12')
			date = date[-4:] + '-' + date[date.index(' ')+1:-5] + '-' + date[:date.index(' ')]
			data[champs_date] = date
		if not re.match(r'^\d{4}-\d{1,2}-\d{1,2}$',date, re.UNICODE):
			if dateTextIsBlank :
				data[champs_date+'_text'] = date
				data[champs_date+'_isComplete'] = False
				dateTextIsBlank = False
			data[champs_date] = '1700-01-01'			
	return data