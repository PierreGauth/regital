#-*- coding: utf-8 -*-
from navigation.models import *
from django import forms
from django.forms.models import modelform_factory

# définition de tous les formulaires associés au modèle (un par classe)

PersonneForm = modelform_factory( Personne,  
  widgets={
    'nom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom', 'onblur' :'recupPersonneInfo()'}),
    'prenom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Prénom', 'onblur' :'recupPersonneInfo()'}),
    'pseudonyme': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Pseudonyme'}),
    'uri_cesar': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Cesar'}),
    'genre': forms.RadioSelect(attrs={'class' : 'radio inline'}),
    'nationalite': forms.Select(attrs={'class' : 'form-control'}),
    'titre_personne': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre', 'name' : 'titre_personne'}),
    'date_de_naissance': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpersonne1' }),
    'date_de_deces': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpersonne2'}),
    'plus_dinfo': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'prenom': 'Prénom',
    'date_de_deces': 'Décès',
    'date_de_naissance': 'Naissance',
  })
    
PieceForm = modelform_factory( Piece,  
  widgets={
    'titre': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre', 'onblur' :'recupPieceInfo()'}),
    'titre_brenner': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre Brenner'}),
    'uri_theaville': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Theaville'}),
    'date_premiere': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpiece1' }),
    'langue': forms.Select(attrs={'class' : 'form-control'}),
    'auteurs': forms.Select(attrs={'class' : 'form-control'}),
    'commentaire': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'date_premiere': 'Première',
    'titre_brenner': 'Titre Brenner',
    'uri_theaville': 'Uri Theaville'
  })   
    
SoireeForm = modelform_factory( Soiree,
  fields=('date', 'libelle_date_reg'),
	widgets={
		'date': forms.TextInput(attrs={'class' : 'form-control', 'value' : '1700-01-01', 'id' : 'dsoiree1' }),
		'libelle_date_reg': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Date de la soiree(version originale)'}),
	},
  labels={
    'libelle_date_reg': 'Date Registre'
  }
)
  
BudgetSoireeForm = modelform_factory( BudgetSoiree,
  fields=('credit_final_reg', 'debit_initial_reg','montant_cachet','montant_cachet_auteur','nb_total_billets_vendus_reg','nombre_cachets','quart_pauvre_reg','credit_total_reg','debit_total_reg','reste_reg','total_depenses_reg','total_recettes_reg','debit_derniere_soiree_reg','total_depenses_corrige_reg'),
	widgets={
		'credit_final_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Crédit final'}),
		'debit_initial_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit initial'}),
		'montant_cachet': forms.Select(attrs={'class' : 'form-control'}),
		'montant_cachet_auteur': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant cachet de l\'auteur'}),
		'nb_total_billets_vendus_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre total de billets vendus'}),
		'nombre_cachets': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre de cachets'}),
		'quart_pauvre_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Quart du pauvre'}),
		'credit_total_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Crédit total'}),
		'debit_total_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit total'}),
		'reste_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Reste'}),
		'total_depenses_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Total dépenses'}),
		'total_recettes_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Total recettes'}),
		'debit_derniere_soiree_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit dernière soirée'}),
		'total_depenses_corrige_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Dépenses corrigées'}),
	},
	labels={
    'credit_final_reg':'Crédit Final', 
    'debit_initial_reg':'Débit Initial',
    'montant_cachet':'Montant Cachet',
    'montant_cachet_auteur':'Montant Cachet Auteur',
    'nb_total_billets_vendus_reg':'Total Billets Vendus',
    'nombre_cachets':'Nombre Cachets',
    'quart_pauvre_reg':'Quart Pauvre',
    'credit_total_reg':'Credit Total',
    'debit_total_reg':'Debit Total',
    'reste_reg':'Reste',
		'total_depenses_reg': 'Total Dépenses',
		'total_recettes_reg': 'Total Recettes',
		'montant_cachet': 'Cachet',
		'montant_cachet_auteur': 'Cachet Auteur',
		'debit_derniere_soiree_reg': 'Débit dernière soirée',
		'total_depenses_corrige_reg': 'Dépenses corrigées',
	}
)  

PageRegistreForm = modelform_factory(PageRegistre,
  fields=('ref_registre','num_page_pdf','redacteurs'),
  widgets={
    'ref_registre' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Référence Registre'}),
    'num_page_pdf' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Numéro page du PDF'}),
		'redacteurs' : forms.Select(attrs={'class' : 'form-control'}),
  },
  labels={
    'ref_registre':'Référence Registre',
    'num_page_pdf':'Numéro page PDF',
  }
)

DebitForm = modelform_factory(Debit,
  fields=('montant','libelle','type_depense','traduction','mots_clefs'),
  widgets={
    'montant': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant'}),
    'libelle' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Libellé'}),
    'type_depense' : forms.Select(attrs={'class' : 'form-control'}),
    'traduction' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Traduction'}),
    'mots_clefs' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Mots clefs'}),
  },
  labels={
    'montant':'',
    'libelle':'',
    'type_depense':'Type de dépense',
    'traduction':'',
    'mots_clefs':'',
  }
)

CreditForm = modelform_factory(Credit,
  fields=('montant','libelle'),
  widgets={
    'montant': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant'}),
    'libelle' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Libellé'}),
  },
  labels={
    'montant':'',
    'libelle':'',
  }
)

BilletterieForm = modelform_factory(Billetterie,
  fields=('montant','libelle','nombre_billets_vendus','type_billet','commentaire'),
  widgets={
    'montant': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant'}),
    'libelle' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Libellé'}),
    'nombre_billets_vendus' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre de billets vendus'}),
    'type_billet' : forms.Select(attrs={'class' : 'form-control'}),
    'commentaire' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Commentaire'}),
  },
  labels={
    'montant':'',
    'libelle':'',
    'nombre_billets_vendus':'',
    'type_billet':'Type billet',
    'commentaire':'',
  }
)

RepresentationForm = modelform_factory(Representation,
  fields=('position','piece'),
  widgets={
    'position': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Position'}),
    'piece' : forms.Select(attrs={'class' : 'form-control'}),
  },
  labels={
  }
)
AnimationForm = modelform_factory(Animation,
  fields=('position','type','auteur','description'),
  widgets={
    'position': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Position'}),
    'type' : forms.Select(attrs={'class' : 'form-control'}),
    'auteur' : forms.Select(attrs={'class' : 'form-control'}),
    'description' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Description'}),
  },
  labels={
  }
)

TransactionSoireeForm = modelform_factory(TransactionSoiree)
TransactionAbonnementForm = modelform_factory(TransactionAbonnement)
AbonnementForm = modelform_factory(Abonnement)
RecapitulatifForm = modelform_factory(Recapitulatif)
DebitRecapitulatifForm = modelform_factory(DebitRecapitulatif)
CreditRecapitulatifForm = modelform_factory(CreditRecapitulatif)
RoleForm = modelform_factory(Role)