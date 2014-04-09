function recupPieceInfo() { 
  var titre = document.getElementsByName("titre")[0].value;
  //var prenom = document.getElementsByName("auteur")[0].value; 
  if (titre != "") { 
    $.get( "../saisie/info/piece/"+titre, function( data ) 
        {
					if(data.indexOf("Aucune Piece ne correspond") == -1) {
          	addTopieceModal("La piece que vous etes en train d\'enter correspond-t-elle à l\'une de ces pieces ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data.replace(/@/g,"'"));
						document.getElementById("azpiece").innerHTML="<div class='alert alert-info'>Nous avons trouvé des pieces similaires sur Theaville.org <button class='btn btn-info' onclick='lauchPieceModal();''>Voir</button></div>";
					}
        });
     }
}         

function lauchPieceModal() {
	tooglepieceModal();
	document.getElementById('azpiece').innerHTML='';
}

function parsePieceInfo(data) {
		var values = data.split(';');                  
    setValue('titre',values[1]);  
		setValue('auteurs',values[3]);                                                            
    setValue('date_premiere',values[2]);              
    setValue('uri_theaville','http://theaville.org/index.php?r=pieces/auteurs/details.php&amp;id='+values[0]);
    tooglepieceModal();
}