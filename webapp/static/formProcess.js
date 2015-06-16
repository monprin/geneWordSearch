function handleForm() {
	// Pull in all the arguments to variables to do the sifting
	var species = document.forms["geneForm"]["species"].value;
	var geneList = document.forms["geneForm"]["genes"].value;
	var probCut = document.forms["geneForm"]["probCut"].value;
	var geneDB = document.forms["geneForm"]["geneDB"].files;
	
	// Get rid of old failed input warnings
	if ($('#fail-warning').length > 0){$('#fail-warning').remove();}
	
	// Deal with bad input
	if(species == null || species == ""){
	// If the species is not specified, return an alert
		$("#titlehead").after('<div class="alert alert-danger container" id="fail-warning">You must select the species.</div>');
		return false;}
	else if(geneList == null || geneList == ""){
	// If no genes are specefied, return an error
		$("#titlehead").after('<div class="alert alert-danger container" id="fail-warning">You must enter at least one gene.</div>');
		return false;}
	else if(species == "other" && geneDB.length == 0){
	// If no geneDBs are specefied and are needed, return an error
		$("#titlehead").after('<div class="alert alert-danger container" id="fail-warning">You must either upload a file to use as the database or select one of the availible species.</div>');
		return false;}
	
	// If everything is in order, run the analysis
	if(species == 'other') {customDB(geneDB,geneList,probCut);}
	else {builtInDB(species,geneList,probCut);}
	
	// When the analysis is done, write the results to the page.
	// If there is a table on the page already, remove it
	
	
	return false;
}

function builtInDB(species,geneList,probCut){
	$.post(($SCRIPT_ROOT + "/_gene_analysis"),{species: species, geneList: geneList, probCut: probCut})
	.done(function(data){tableMaker(data.result);});
	return;
}

function customDB(geneDB,geneList,probCut){
	$.post(($SCRIPT_ROOT + "/_custom_db_analysis"),{species: species, geneList: geneList, probCut: probCut})
	.done(function(data){tableMaker(data.result);});
	return;
}

function tableMaker(JSONResults){
	if ($('#results').length <= 0){
		$('#geneFormCont').after('<div class="container"><h2 id="results_head">Results:</h2><br><table cellpadding="0" cellspacing="0" border="0" class="table table-hover" id="results"><thead><tr><th>Word</th><th>P Value</th><th>Corrected P Value</th><th>Overlap</th></tr></thead></table></div>');}
	else{var table = $('#results').DataTable();table.destroy();}
	
	$('#results').DataTable({
			"data": JSON.parse(JSONResults),
			"order": [[1,'asc']],
			"columns":
				[{"data": "word"},
				{"data": "pval"},
				{"data": "corpval"},
				{"data": "overlap"}]});
	return;
}




