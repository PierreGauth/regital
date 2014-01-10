from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from dataManager.importer import Importer

def index(request):
    return HttpResponse("Bienvenue dans la saisie.")
	
def detail(request, saisie_id):
    return HttpResponse("You're looking at poll %s." % saisie_id)

def results(request, saisie_id):
    return HttpResponse("You're looking at the results of poll %s." % saisie_id)

def vote(request, saisie_id):
    return HttpResponse("You're looking at poll %s." % saisie_id)
	
def importation(request):
	importer = Importer()
	#return HttpResponse("Imported : %s" % importer.importYaml('dataManager/personne_regital_yaml.yml'))
	return HttpResponse("%s" % importer.importYaml('dataManager/yaml_pivot_2.yml'))
	
def test(request):
	importer = Importer()
	return HttpResponse("%s" % importer.recreateYaml('dataManager/yaml_pivot_2.yml').replace("}", "}<br/>").replace("-", "<br/>-"))