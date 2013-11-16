# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from dataManager.models import *
import yaml
#from models import *

class Importer:
	def __init__(self):
		self.data = []
	def importYaml(self, yamlfile):
		yamlInfo = {}
	
		for yamlInfo in yaml.load_all(file(yamlfile, 'r')):
			#self._import(yamlInfo)
			return yamlInfo 
				
	def _import(self, yamlData, key):
	
		createInstance = "class = " + slef._to_class_name(key) + "("
		
		for attribute in yamlData.iterkeys():
			if not isinstance(yamlData, (list, tuple, dict)): #si c'est une variable simple
				createInstance = createInstance + slef._to_attribute_name(attribute) + "=yamlData['" + attribute + "'],"
			else:
				createInstance = createInstance + slef._to_attribute_name(attribute) + "=slef._import(yamlData['" + attribute + "'], " + attribute + "),"
			
		createInstance = createInstance + ")\nclass.save()"
		createInstance = createInstance.replace(",)", ")")
		
		print createInstance + "\n\n"
		#exec createInstance		 

		
	def _to_class_name(value):
		def camelcase(): 
			yield str.lower
			while True:
				yield str.capitalize

		c = camelcase()
		return "".join(c.next()(x) if x else ' ' for x in value.split(" "))
	
	def _to_attribute_name(value):
		def camelcase(): 
			yield str.lower
			while True:
				yield str.capitalize

		c = camelcase()
		return "".join(c.next()(x) if x else ' ' for x in value.split(" "))
		
	