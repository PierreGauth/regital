#-*- coding: utf-8 -*-
 
import re
import requests
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse     
 
def searchPersonne(request, titre='', auteur=''):        
#    payload = {'r': 'piece', 'titre': titre, 'auteur': auteur,'crea_de_annee':'1709','crea_a_annee':'1794',
#                'rep_de_annee':'1709', 'rep_a_annee':'1794', 'lieu':'', 'cible':'', 'source':''}
#    r = requests.get("http://www.theaville.org/kitesite/index.php", params=payload, 
##       proxies= 
##       {
##         "http": "http://cache.wifi.univ-nantes.fr:3128",
##         "https": "http://cache.wifi.univ-nantes.fr:3128",
##       }
#    )
#    page = r.text
     page = getPage1()
    
    page = page[page.index("<!--   Document   -->"):page.index("<script>")]
    if not '0 records matched your query' in page :   
      page = page[page.index("<TR"):page.index("</TABLE")]
      page = page.replace(u'<A HREF=\'../people/people.php?fct=edit&person_UOID=',u'<button type="button" class="btn" onClick=\'parsePersonneInfo(')
      pattern = '\'>\w*</A>'
      pattern = re.compile(pattern, re.UNICODE)
      page = pattern.sub(u")'> <span class='glyphicon glyphicon glyphicon-arrow-right'></span></button>",page)
      return HttpResponse("<table>" + page+ "</table>", content_type="text/plain")
    else:
      return HttpResponse('Aucune Personne ne correspond à ce nom sur cesar.org.uk', content_type="text/plain")
    
def getInfoPersonne(request, id):
    payload = {'fct': 'edit', 'person_UOID': id }
    r = requests.get("http://www.cesar.org.uk/cesar2/people/people.php", params=payload 
      # ,proxies= 
      # {
        # "http": "http://cache.wifi.univ-nantes.fr:3128",
        # "https": "http://cache.wifi.univ-nantes.fr:3128",
      # }
    )
    page = r.text
    # page = getPage2()
    
    page = page[page.index("<H1>People</H1>"):page.index("<H2>Notes</H2>")] 
    infos = ''
    
    for i in range(1,10):
      page = page[page.index('keyColumn')+1:]
      if i == 8 :
        infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-23]
      elif (i == 7) or (i == 6) : #si c'est une date
        infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-29]
      else:
        infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-29]
    
    return HttpResponse(infos, content_type="text/plain")    

def getPage1() :
  return '''
  

<div id="document">

<!--   Document   -->


<small>Liste | <a href="index.php?r=pieces/cibles">Cibles</a> | <a href="index.php?r=pieces/lieux">Lieux</a> | <a href="index.php?r=pieces/auteurs">Auteurs&nbsp;</a></small><br /><br />

<h1 class="invisible">Liste des pi&egrave;ces</h1>

<p></p><strong>1 r&eacute;sultat&nbsp;:</strong></p>
<table id="table" class="pieces">
<thead>
  <tr>
    <th>Titre&nbsp;</th>
    <th>Parodie de&nbsp;</th>
    <th>Cr&eacute;ation&nbsp;</th>
    <th>Auteur(s)&nbsp;</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=2">Achille et Déidamie</a></td>
    <td><em>Achille et Déidamie</em> de Danchet et Campra</td>
    <td>1735</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=74">Riccoboni (François) dit Lélio fils<br />
<a href="index.php?r=pieces/auteurs/details.php&amp;id=77">Romagnesi (Jean-Antoine)</td>
  </tr>
</tbody>
</table>
<br />

<script>


  '''

def getPage2() :
  return '''

<H1>People</H1>

 
 
<TABLE WIDTH='100%' CELLPADDING=2 CELLSPACING=2 BORDER=0>
<TR><TD ID='objectSummary'>Mlle Marie-Anne-Xavier <B> Mathieu </B><I>dite Testard </I>(1746 - )</TD></TR>
</TABLE>
<P>
<TABLE WIDTH='100%' CELLPADDING='0' CELLSPACING='2' BORDER='0'>
<TR><TD ID='keyColumn'>&nbsp;Titre&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Mlle&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Prénom&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Marie-Anne-Xavier&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Particule&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Nom de famille&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Mathieu&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Date de naissance&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;1746&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Date de décès&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Pseudonyme&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Testard&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Sexe&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;female</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Nationalité&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;French&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Compétences&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Danseur(euse)</TD></TR>
</TABLE>

<P><HR><H2>Notes</H2><P>
<H3>Campardon</H3><UL>
L'Académie royale de musique au XVIIIe siècle, 1884, t. II, p. 304 : 
"danseuse, née à Rouen, vers 1746. Avant d'appartenir à l'Académie royale de musique, où elle figura pendant les années 1769 et 1770, 
elle avait été attachée aux corps de ballet de l'Opéra-Comique et de la Comédie-Française (…)" [AS]

</UL>
</P>

'''