from django.db import models
from django.db.models.signals import pre_init
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms

### définition du modèle de données

### Gestion des supports physiques (registres)

class PageRegistre(models.Model):
	ref_registre = models.CharField(max_length=64, null=False)
	num_page_pdf = models.IntegerField()
	class Meta:
		unique_together = ('ref_registre', 'num_page_pdf',)

	def __unicode__(self):
		return 'Registre {0.ref_registre!r} page {0.num_page_pdf!s}'.format(self)

### Gestion financière

class Transaction(models.Model): # relevé de compte
	T_MONNAIE = (
	    ('£', 'livre (£)'),
	    ('S', 'sou (S)'),
	    ('d', 'denier (d)'),
	)
	class Meta:
		abstract = True

	date = models.DateField('date', null=False)
	libelle = models.CharField(max_length=64)
	montant = models.IntegerField(null=True, blank=True) # + ou - selon crédit/débit
	monnaie = models.CharField(max_length=1, choices=T_MONNAIE, default='d', blank=True)
	encours = models.IntegerField(null=True, blank=True) # attribut calculé, pour suivi de compte à tout instant

	def __unicode__(self):
		return '{0.date!s} - {0.libelle}: {0.montant!s}'.format(self)

class TransactionSoiree(Transaction):
	budget = models.OneToOneField('BudgetSoiree')

	def __unicode__(self):
		return '{}'.format(super)

class TransactionAbonnement(Transaction): 		
	paiement_abonnement = models.ForeignKey('Abonnement') # 1 abonnement est payé en plusieurs fois

	def __unicode__(self):
		return '{}'.format(super)

		
class BudgetSoiree(models.Model):
	T_SALAIRE = (
	    (' 6 ', '1440'),
	    (' 9 ', '2160'),
	    ('12 ', '2880'),
	    ('12¼', '2940'),
	    ('12½', '3000'),
	    ('13 ', '3120'),
	    ('13¾', '3300'),
	    ('14 ', '3360'),
	    ('14¾', '3540'),
	    ('15 ', '3600'),
		('err', '-1')
	)
	total_depenses = models.IntegerField(null=True, blank=True) # attribut calculé
	nb_total_billets_vendus = models.IntegerField(null=True, blank=True) # attribut calculé
	total_recettes = models.IntegerField(null=True, blank=True) # attribut calculé
	total_depenses_reg = models.IntegerField()
	nb_total_billets_vendus_reg = models.IntegerField(null=True, blank=True)
	total_recettes_reg = models.IntegerField()	# recette des billets, égale au crédit (BW) ?
	debit_derniere_soiree_reg = models.IntegerField(null=True, blank=True)	# dette héritée de la précédente soirée, vide sinon.
	total_depenses_corrige_reg = models.IntegerField(null=True, blank=True)	# dépenses + débit dernière soirée
	quart_pauvre_reg = models.IntegerField(null=True, blank=True)	# impôt sur la recette (calculé comment ?)
	debit_initial_reg = models.IntegerField(null=True, blank=True)	# quart du pauvre + total dépenses corrigé
	reste_reg = models.IntegerField(null=True, blank=True)	# |recette billets - débit initial (quart du pauvre + total dépenses corrigé)|
	debit_total_reg = models.IntegerField(null=True, blank=True) 	# ???
	credit_total_reg = models.IntegerField(null=True, blank=True)	# ???
	nombre_cachets = models.FloatField(null=True, blank=True) # nombre de personnes rémunérées (hors auteurs)
	montant_cachet = models.CharField(max_length=3, choices=T_SALAIRE) # montant du cachet, identique pour tous (sauf auteurs)
	montant_cachet_auteur = models.IntegerField(null=True, blank=True)	# montant du cachet aux auteurs (par auteur ?) - s'ajoute à la "masse salariale"
	# (montant_cachets * nbre_cachets) + (m_c_auteur * nbre_auteurs) = montant des salaires
	# Attention : en cas de solde négatif, les cachets déclarés sont versés au cours de la soirée suivante (avec solde positif) !
	credit_final_reg = models.IntegerField(null=True, blank=True)	# reste - salaires, vide si solde est négatif pour la soirée
	# où va cet argent ('avanza') ? On ne le retrouve pas ensuite...
	redacteurs = models.ManyToManyField('Personne', null=True, blank=True) # class Personne pas encore déclarée
	page_registre = models.OneToOneField(PageRegistre)

	def __unicode__(self):
		return 'Le {0.Soiree.date}: Dépenses={0.total_depenses_reg!s} | Recettes={0.total_recettes_reg!s}'.format(self)

def pre_init_budget( **kwargs):
	attributes = kwargs['kwargs']
	if 'ref_registre' in attributes :
		attributes['page_registre'] = PageRegistre(ref_registre = attributes['ref_registre'], num_page_pdf = attributes['num_page_pdf'])
		del attributes['ref_registre']
		del attributes['num_page_pdf']
	if 'credit_final' in attributes:
		attributes['credit_final_reg'] = attributes['credit_final']
		del attributes['credit_final']
	if 'credit' in attributes:
		# attributes['credit_reg'] = attributes['credit']
		del attributes['credit']
	if 'quart_pauvre' in attributes:
		attributes['quart_pauvre_reg'] = attributes['quart_pauvre']
		del attributes['quart_pauvre']
	if 'reste' in attributes:
		attributes['reste_reg'] = attributes['reste']
		del attributes['reste']
	if 'debit_derniere_soiree' in attributes:
		attributes['debit_derniere_soiree_reg'] = attributes['debit_derniere_soiree']
		del attributes['debit_derniere_soiree']		
	if 'debit_initial' in attributes:
		attributes['debit_initial_reg'] = attributes['debit_initial']
		del attributes['debit_initial']
	if 'total_depenses_corrige' in attributes:
		attributes['total_depenses_corrige_reg'] = attributes['total_depenses_corrige']
		del attributes['total_depenses_corrige']
	if 'recette_billets_vendus' in attributes:
		attributes['total_recettes'] = attributes['recette_billets_vendus']
		del attributes['recette_billets_vendus']
	if 'anecdote' in attributes:
		del attributes['anecdote']
	kwargs['kwargs'] = attributes
		
pre_init.connect(pre_init_budget, BudgetSoiree)

class Abonnement(models.Model):
	debut = models.DateField()
	fin = models.DateField()
	tarif = models.IntegerField()
	abonne = models.ForeignKey('Personne')

	def __unicode__(self):
		return 'Abonnement du {0.debut!s} au {0.fin!s} pour la somme de {0.montant!s}d'.format(self)


# récapitualif "hors compte", non associé à une transaction	
class Recapitulatif(models.Model):
	T_RECAPITULATIF = (
	    (0, 'hebdomadaire'),
	    (1, 'bimensuel'),
	    (2, 'mensuel'),
	    (3, 'bimestriel'),
	    (4, 'trimestriel'),
	    (5, 'semestriel'),
	    (6, 'annuel'),
	)
	date = models.DateField() # date de réalisation du récapitulatif couvrant la période précédente
	frequence = models.IntegerField(null=False, choices=T_RECAPITULATIF, default=2)
	total_depenses = models.IntegerField(null=True, blank=True) # attribut calculé
	total_recettes = models.IntegerField(null=True, blank=True) # attribut calculé
	total_depenses_reg = models.IntegerField()
	total_recettes_reg = models.IntegerField()
	total_depenses_divers_reg = models.IntegerField()
	monnaie = models.CharField(max_length=1, choices=Transaction.T_MONNAIE, default='d')
	page_registre = models.OneToOneField(PageRegistre)
	redacteurs = models.ManyToManyField('Personne', null=True, blank=True) # class Personne pas encore déclarée
#	transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
	class Meta:
		unique_together=(('date', 'frequence',),)

	def __unicode__(self):
		return 'Bilan {0.frequence} du {0.date!s}: Dépenses={0.total_depenses_reg!s}d | Recettes={0.total_recettes_reg!s}d'.format(self)
	

class CreditRecapitulatif(models.Model):
	montant = models.IntegerField()
	libelle = models.CharField(max_length=64)
	bilan = models.ForeignKey(Recapitulatif)

	def __unicode__(self):
		return '{0.libelle}: {0.montant!s}d'.format(self)


class DebitRecapitulatif(models.Model):
	montant = models.IntegerField()
	libelle = models.CharField(max_length=64)
	bilan = models.ForeignKey(Recapitulatif)

	def __unicode__(self):
		return '{0.libelle}: {0.montant!s}d'.format(self)


class Credit(models.Model):
	montant = models.IntegerField(null=False)
	libelle = models.CharField(max_length=64, null=True, blank=True)
	budget = models.ForeignKey(BudgetSoiree)

	def __unicode__(self):
		return '{0.libelle}: {0.montant!r}d'.format(self)
	
	
class Billetterie(Credit):	# relation d'héritage (sous-classe de)
	T_BILLET = (
	    (0, 'parterre'),
	    (1, 'première loge'),
	    (2, 'balcon 1ère loge'),
	    (3, 'deuxième loge'),
	    (4, 'balcon 2ème loge'),
	    (5, 'troisième loge'),
	    (6, 'paradis'),
		(7, 'supplément'),
		(8, 'prima loggia'),
		(9, 'seconda loggia'),
		(10, 'personnalité'),
	)
	nombre_billets_vendus = models.IntegerField(null=True, blank=True)
	type_billet = models.IntegerField(choices=T_BILLET, null=False)
	commentaire = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return '{0.type_billet!r}: {0.nombre_billets_vendus} billet(s) pour {0.montant}d'.format(self)
	
	# def validate_unique(self, *args, **kwargs):
	# 	super(Billetterie, self).validate_unique(*args, **kwargs)
	# 	
	# 	if self.__class__.objects.filter(budget=self.budget, type_billet=self.type_billet).exists():
	# 		raise ValidationError({NON_FIELD_ERRORS: ('Billeterie object already exists.',),})	

def pre_init_billetterie( **kwargs):
  attributes = kwargs['kwargs']
  if 'type' in attributes :
    attributes['type_billet'] = 2#attributes['type']
    del attributes['type']
  if 'billets' in attributes :
    attributes['nombre_billets_vendus'] = attributes['billets']
    del attributes['billets']
  if 'recette' in attributes :
    attributes['montant'] = attributes['recette']
    del attributes['recette']
  kwargs['kwargs'] = attributes
		
pre_init.connect(pre_init_billetterie, Billetterie)

	
class Debit(models.Model):
	T_DEPENSE = (
	    (0, 'ordinaire'),
	    (1, 'vivant'),
	    (2, 'accessoire'),
	    (3, 'musique'),
	    (4, 'divers'),
		(5, 'indéterminé')
	)
	montant = models.IntegerField(null=False)
	libelle = models.CharField(max_length=64, blank=True)
	type_depense = models.IntegerField(choices=T_DEPENSE, default=5, blank=True)
	budget = models.ForeignKey(BudgetSoiree)
	traduction = models.CharField(max_length=64, null=True, blank=True)
	mots_clefs = models.CharField(max_length=64, null=True, blank=True)

	class Meta:
		unique_together=(('libelle', 'budget', 'montant', 'type_depense',),)
		
	def __unicode__(self):
		return '{0.type_depense!r}: {0.libelle} pour {0.montant}d'.format(self)

		
### Gestion des soirées : unité élémentaire du modèle de données

class Soiree(models.Model):
	date = models.DateField(unique=True)
	libelle_date_reg = models.CharField(max_length=64)
	budget = models.OneToOneField(BudgetSoiree, null=True, blank=True)
	ligne_src = models.IntegerField(null=False)

	def __unicode__(self):
		return 'Soiree du {0.date} '.format(self)
		
def pre_init_soiree( **kwargs):
	attributes = kwargs['kwargs']
	attributes['ligne_src'] = 123
	kwargs['kwargs'] = attributes
		
pre_init.connect(pre_init_soiree, Soiree)
	
	
class Representation(models.Model):
	piece = models.ForeignKey('Piece')
	Soiree = models.ForeignKey(Soiree)
	position = models.IntegerField(null=True, blank=True) # ordre de passage dans la soirée
	roles = models.ManyToManyField('Personne', through='Role')
	class Meta:
		unique_together=(('piece', 'Soiree', 'position'),)

	def __unicode__(self):
		return 'La pièce {0.piece.titre!r} jouée le {0.Soiree.date!s} ({0.position!s})'.format(self)

def pre_init_representation( **kwargs):
	attributes = kwargs['kwargs']
	piece = attributes.get('piece')
	newAttributes = {}
	if not isinstance(piece, Piece):
		newAttributes['piece'] = Piece(attributes)
		newAttributes['position'] = attributes.get('position')
		newAttributes['Soiree'] = attributes.get('Soiree')
		kwargs['kwargs'] = newAttributes
		print kwargs
		
pre_init.connect(pre_init_representation, Representation)

class Animation(models.Model):
	T_ANIMATION = (
	    (0, 'divertissement'),
	    (1, 'feu d\'artifice'),
	    (2, 'compliment'),
	)
	Soiree = models.ForeignKey(Soiree)
	position = models.IntegerField() # ordre de passage dans la soirée
	type = models.IntegerField(choices=T_ANIMATION)
	auteur = models.ForeignKey('Personne', null=True, blank=True) # pour compliment, null sinon
	description = models.TextField(blank=True) # pour divertissement, '' sinon
	class Meta:
		unique_together=(('type', 'Soiree', 'position'),)
	
	def __unicode__(self):
		return 'Un {0.type_animation} est donné le {0.Soiree.date!s} ({0.position!s})'.format(self)

def pre_init_animation( **kwargs):
	attributes = kwargs['kwargs']
	auteur = attributes.get('auteur')	
	if not isinstance(auteur, Personne):
		attributes['auteur'] = Personne.objects.get(nom=auteur)
	# if 'type' in attributes :
		# attributes['type'] = T_ANIMATION(attributes['type'])
		# del attributes['type']
	kwargs['kwargs'] = attributes
		
pre_init.connect(pre_init_animation, Animation)
	
### Gestion des pièces et des ressources humaines

class Personne(models.Model):
	T_GENRE = (
		('M', 	'homme'),
		('F', 	'femme'),
		('-', 	'indéterminé'),
	)
	T_NATIONALITE = (
		('fr', 	'française'),
		('it', 	'italienne'),
		('de', 	'allemande'),
		('en', 	'anglaise'),
		('-',	'indéterminée')
	)
	nom = models.CharField(max_length=64, null=False)
	prenom = models.CharField(max_length=64, blank=True)
	pseudonyme = models.CharField(max_length=64, blank=True) # pour les acteurs essentiellement
	uri_cesar = models.URLField(max_length=256, null=True, blank=True)
	genre = models.CharField(max_length=1, choices=T_GENRE, default='-', blank=False)
	nationalite = models.CharField(max_length=3, choices=T_NATIONALITE, default='-', blank=False)
	titre = models.CharField(max_length=64, blank=True)
	date_de_naissance = models.DateField(null=True, blank=True)
	date_de_deces = models.DateField(null=True, blank=True)
	plus_dinfo = models.TextField(null=True, blank=True)
	class Meta:
		unique_together=(('nom', 'prenom', 'date_de_naissance', 'genre'),)

	def __unicode__(self):
		return '{0.prenom} {0.nom}'.format(self)

	
class Piece(models.Model):
	T_LANGUE = (
	    ('fr', 		'français'),
	    ('it', 		'italien'),
		('it/fr', 	'italien et français'),
		('-', 		'indéterminé')
	)
	titre = models.CharField(max_length=128)
	titre_brenner = models.CharField(max_length=128, null=True, blank=True)
	uri_theaville = models.URLField(max_length=256, null=True, blank=True)
	date_premiere = models.DateField(null=True, blank=True)
	langue = models.CharField(max_length=5, choices=T_LANGUE, default='-', blank=True)
	commentaire = models.TextField(null=True, blank=True) # pour consigner les anecdotes
	auteurs = models.ManyToManyField(Personne, null=True, blank=True)

	def __unicode__(self):
		return '{0.titre_brenner!r} ({0.titre})'.format(self)

	class Meta:
		unique_together=(('titre_brenner', 'date_premiere',),)

#	def validate_unique(self, *args, **kwargs):
#		super(Piece, self).validate_unique(*args, **kwargs)
#		if self.__class__.objects.filter(titre=self.titre, auteurs__in=self.auteurs.all()).exists():
#			raise ValidationError({NON_FIELD_ERRORS: ('Piece object already exists.',),})

# def pre_init_piece( **kwargs):
	# attributes = kwargs['kwargs']
	# if 'auteurs' in attributes :
		# del attributes['auteurs']
	# if 'premiere_representation' in attributes :
		# attributes['date_premiere'] = attributes['premiere_representation']
		# del attributes['premiere_representation']
	# if 'position' in attributes :
		# del attributes['position']
	# kwargs['kwargs'] = attributes
		
# pre_init.connect(pre_init_piece, Piece)
	

# table d'association avec attributs d'association
# un même individu peut jouer plusieurs rôles lors d'une représentation
class Role(models.Model):
	personne = models.ForeignKey(Personne)
	representation = models.ForeignKey(Representation)
	role = models.CharField(max_length=64) # acteur, musicien, souffleur, danseur, chanteur, +rôles des pièces
	plus_dinfo = models.TextField() # pour préciser l'instrument du musicien, etc.
	class Meta:
		unique_together=(('personne', 'representation', 'role'),)

	def __unicode__(self):
		return 'Rôle {0.role} par {0.personne.prenom} {0.personne.nom} dans {0.representation}'.format(self)


# définition de tous les formulaires associés au modèle (un par classe)
from django.forms.models import modelform_factory

# class PersonneForm(forms.ModelForm):
    # class Meta:
        # model = Author
        # fields = ('name', 'title')

    # def clean_name(self):
        # # custom validation for the name field
        # ...



# class PersonneForm(forms.Form):
    # nom = forms.CharField(label='Nom', forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom'}))        
    
PersonneForm = modelform_factory( Personne,  
  widgets={
    'nom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom'}),
	'prenom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Prénom'}),
	'pseudonyme': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Pseudonyme'}),
	'uri_cesar': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Cesar'}),
	'genre': forms.RadioSelect(attrs={'class' : 'radio inline'}),
	'nationalite': forms.Select(attrs={'class' : 'form-control'}),
	'titre': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre'}),
	'date_de_naissance': forms.TextInput(attrs={'class' : 'form-control', 'value':'02-16-2012', 'id' : 'dp1' }),
	'date_de_deces': forms.TextInput(attrs={'class' : 'form-control', 'value':'02-16-2012', 'id' : 'dp2'}),
	'plus_dinfo': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'prenom': 'Prénom',
  })
    
PageRegistreForm = modelform_factory(PageRegistre)
TransactionSoireeForm = modelform_factory(TransactionSoiree)
TransactionAbonnementForm = modelform_factory(TransactionAbonnement)
BudgetSoireeForm = modelform_factory(BudgetSoiree)
AbonnementForm = modelform_factory(Abonnement)
RecapitulatifForm = modelform_factory(Recapitulatif)
DebitRecapitulatifForm = modelform_factory(DebitRecapitulatif)
CreditRecapitulatifForm = modelform_factory(CreditRecapitulatif)
DebitForm = modelform_factory(Debit)
CreditForm = modelform_factory(Credit)
BilletterieForm = modelform_factory(Billetterie)
SoireeForm = modelform_factory(Soiree)
RepresentationForm = modelform_factory(Representation)
AnimationForm = modelform_factory(Animation)
PieceForm = modelform_factory(Piece)
RoleForm = modelform_factory(Role)
