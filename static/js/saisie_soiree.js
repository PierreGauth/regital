function addPersonne() {
	
	$('#personneFormButton').attr('type', 'button');
	$('#personneFormButton').attr('onclick', 'createPersonne();');
	$('#personneForm').attr('action', '/saisie/new/personne/Soiree');
  $('#myTab a[href="#Personne"]').tab('show');
}         

function createPersonne() {
	
	soireeValue = 
	$('#personneForm').append('<div style="visibility:hidden;">'
		+ $('#soireeForm').html()
		+'</div');
	$('#personneForm').submit();
}

function addPiece() {
	
  $('#myTab a[href="#Piece"]').tab('show');
}         

function createPiece() {
}

