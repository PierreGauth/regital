#-*- coding: utf-8 -*-
from navigation.models import *
from django import forms
from django.forms.models import modelform_factory

# définition de tous les formulaires associés au modèle (un par classe)

PersonneForm = modelform_factory( Personne,  
  widgets={
    'nom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom', 'onblur' :'recupInfo()'}),
    'prenom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Prénom', 'onblur' :'recupInfo()'}),
    'pseudonyme': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Pseudonyme'}),
    'uri_cesar': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Cesar'}),
    'genre': forms.RadioSelect(attrs={'class' : 'radio inline'}),
    'nationalite': forms.Select(attrs={'class' : 'form-control'}),
    'titre': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre'}),
    'date_de_naissance': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dp1' }),
    'date_de_deces': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dp2'}),
    'plus_dinfo': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'prenom': 'Prénom',
    'date_de_deces': 'Décès',
    'date_de_naissance': 'Naissance',
  })
    
SoireeForm = modelform_factory( Soiree,
	widgets={
		'date_soiree': forms.TextInput(attrs={'class' : 'form-control', 'value' : '01-01-1750', 'id' : 'dp1' }),
		'libelle_date_soiree_reg': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Date de la soirée(version originale)'}),
	}
)
  
BudgetSoireeForm = modelform_factory( BudgetSoiree,
	widgets={
		'credit_final_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Crédit final'}),
		'debit_initial_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit initial'}),
		'montant_cachet': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant cachet'}),
		'montant_cachet_auteur': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant cachet de l\'auteur'}),
		'nb_total_billets_vendus_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre total de billets vendus'}),
		'nombre_cachets': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre de cachets'}),
		'quart_pauvre_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Quart du pauvre'}),
		'credit_total_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Crédit total'}),
		'debit_total_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit total'}),
		'reste_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Reste'}),
		'total_depenses_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Total dépenses'}),
		'total_recettes_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Total recettes'}),
	},
	labels={
	'credit_final_reg':'Crédit final',
	'debit_initial_reg':'Débit initial',
	'credit_total_reg':'Crédit total',
	'debit_total_reg':'Débit total',
	'total_depenses_reg':'Total dépenses',
	'total_recettes_reg':'Total recettes',
	}
)  

PageRegistreForm = modelform_factory(PageRegistre)
TransactionSoireeForm = modelform_factory(TransactionSoiree)
TransactionAbonnementForm = modelform_factory(TransactionAbonnement)
AbonnementForm = modelform_factory(Abonnement)
RecapitulatifForm = modelform_factory(Recapitulatif)
DebitRecapitulatifForm = modelform_factory(DebitRecapitulatif)
CreditRecapitulatifForm = modelform_factory(CreditRecapitulatif)
DebitForm = modelform_factory(Debit)
CreditForm = modelform_factory(Credit)
BilletterieForm = modelform_factory(Billetterie)
RepresentationForm = modelform_factory(Representation)
AnimationForm = modelform_factory(Animation)
PieceForm = modelform_factory(Piece)
RoleForm = modelform_factory(Role)