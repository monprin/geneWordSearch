function handleForm() {
    // Pull in all the arguments to variables to do the sifting
    var species = document.forms["geneForm"]["species"].value;
    var geneList = document.forms["geneForm"]["genes"].value;
    var probCut = document.forms["geneForm"]["probCut"].value;
    var geneDBs = document.forms["geneForm"]["geneDBs"].files;
    
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
    else if(species == "other" && geneDBs.length == 0){
    // If no geneDBs are specefied and are needed, return an error
        $("#titlehead").after('<div class="alert alert-danger container" id="fail-warning">You must either upload a file to use as the database or select one of the availible species.</div>');
        return false;}
    else if(species == "other" && geneDBs.length > 10){
    // If no geneDBs are specefied and are needed, return an error
        $("#titlehead").after('<div class="alert alert-danger container" id="fail-warning">You may only upload up to 10 database files for an analysis.</div>');
        return false;}
    
    // If everything is in order, run the analysis and write the results
    if(species == 'other') {customDB(geneDBs,geneList,probCut);}
    else {builtInDB(species,geneList,probCut);}
    
    return false;
}

function builtInDB(species,geneList,probCut){
    $.post(($SCRIPT_ROOT + "/_gene_analysis"),{species: species, geneList: geneList, probCut: probCut})
    .done(function(data){tableMaker(data.result);});
    return;
}

function customDB(geneDBs,geneList,probCut){
    var numFiles = geneDBs.length
    var fStrings = []
    var delimiters = []
    var headers = []
    var geneCol = []
    var desCols = []
    for(var i = 0; i < numFiles; i++){
        var fr = new FileReader();
        fr.readAsText(geneDBs[i]);
        var check = function(){
            if(fr.readyState != 2){fStrings.push(String(fr.result));console.log(String(fr.result)+"hey");return;}
            else{setTimeout(check,1000);}}
        if(fr.readyState != 2){check();}
        delete fr;
        delimiters.push(document.forms["geneForm"]["delimiter"+String(i)].value);
        headers.push(document.forms["geneForm"]["header"+String(i)].value);
        geneCol.push(document.forms["geneForm"]["geneCol"+String(i)].value);
        desCols.push(document.forms["geneForm"]["desCols"+String(i)].value);
    }
    $.post(($SCRIPT_ROOT + "/_custom_db_analysis"),
        {geneList: geneList, 
        probCut: probCut,
        fStrings: fStrings,
        delimiters: delimiters,
        headers: headers,
        geneCol: geneCol,
        desCols: desCols})
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

$(function() {
    $(document).on('change.bs.fileinput', '.fileinput', function(e) {
        var $this = $(this),
            $input = $this.find('input[type=file]'),
            $span = $this.find('.fileinput-filename');
        if($input[0].files !== undefined && $input[0].files.length > 1) {
            $span.addClass('dropdown').html('<a href="#" data-toggle="dropdown" class="dropdown-toggle">Multiple files selected <i class="caret"></i></a><ul class="dropdown-menu" role="menu"><li>' + $.map($input[0].files, function(val) { return val.name; }).join('</li><li>') + '</li></ul>');}
        if($input[0].files !== undefined && $input[0].files.length <= 10){
            var numFiles = $input[0].files.length
            $('#dbqs').html('<div id="DBquestionsCont" class="form-group container"><h3>Please answer the following questions about the database files:</h3>');
            for(var i = 0; i < numFiles; i++){
                var namey = $input[0].files[i].name
                $('#dbqs').append('<h4>For "'+namey+'":</h4>');
                $('#dbqs').append('<label class="control-label" for="header'+String(i)+'">Does this table have headers?</label>');
                $('#dbqs').append('<div class="radio-inline"><label><input type="radio" name="header'+String(i)+'" value="y" >Yes</label></div>');
                $('#dbqs').append('<div class="radio-inline"> <label><input type="radio" name="header'+String(i)+'" value="n" >No</label></div><br>');
                if(namey.substr(namey.length-4) == ".tsv"){ 
                    $('#dbqs').append('<label for="delimiter'+String(i)+'">What delimiter does this file use?</label><input type="text" size="4" name="delimiter'+String(i)+'" value="tab" disabled><br>');}
                else if(namey.substr(namey.length-4) == ".csv"){ 
                    $('#dbqs').append('<label for="delimiter'+String(i)+'">What delimiter does this file use?</label><input type="text" size="4" name="delimiter'+String(i)+'" value="," disabled><br>');}
                else{
                    $('#dbqs').append('<label for="delimiter'+String(i)+'">What delimiter does this file use?</label><input type="text" size="4" name="delimiter'+String(i)+'" ><br>');}
                $('#dbqs').append('<label for="geneCol'+String(i)+'">Which column has the gene identifiers (numbering start at 1)?</label><input type="text" size="4" name="geneCol'+String(i)+'" ><br>');
                $('#dbqs').append('<label for="desCols'+String(i)+'">Which columns have the gene descriptions (seprate each number by a space)?</label><br><textarea rows="1" class="form-control" id="desCols'+String(i)+'" form="geneForm" ></textarea><br>');
            }}
        else if($input[0].files !== undefined && $input[0].files.length > 10){alert("You may not upload more than 10 files for use as a database.");}
    });});
    //$(document).ready(function(){$('#remove').click(function(){$('#dbqs').html('<p>hey</p>');})});
    


