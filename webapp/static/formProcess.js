function handleForm() {
    // Pull in all the arguments to variables to do the sifting
    var species = document.forms["geneForm"]["species"].value;
    var geneList = document.forms["geneForm"]["geneList"].value;
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
    // If too many geneDBs are specefied, return an error
        $("#titlehead").after('<div class="alert alert-danger container" id="fail-warning">You may only upload up to 10 database files for an analysis.</div>');
        return false;}
    
    // If everything is in order, run the analysis and write the results
    if(species == 'other') {customDB();}
    else {builtInDB(species,geneList,probCut);}
    
    return false;
}

function builtInDB(species,geneList,probCut){
    $('#waitMSG').removeClass("hidden");
    $.post(($SCRIPT_ROOT + "/_gene_analysis"),{species: species, geneList: geneList, probCut: probCut})
    .done(function(data){tableMaker(data.result);});
    return;
}

function customDB(){
    var fd = new FormData(document.querySelector('#geneForm'));
    $('#waitMSG').removeClass("hidden");
    $.ajax({
        url: ($SCRIPT_ROOT + '/_custom_db_analysis'),
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){tableMaker(data.result);}
        });
    return;}

function tableMaker(JSONResults){
    $('#waitMSG').addClass("hidden");
    if ($('#results').length <= 0){
        $('#waitMSG').after('<div class="container"><h2 id="results_head">Results:</h2><br><table cellpadding="0" cellspacing="0" border="0" class="table table-hover" id="results"><thead><tr><th>Word</th><th>P Value</th><th>Corrected P Value</th><th>Overlap</th></tr></thead></table></div>');}
    else{var table = $('#results').DataTable();table.destroy();}
    
    $('#results').DataTable({
            "data": JSON.parse(JSONResults),
            "order": [[1,'asc']],
            "columns":
                [{"data": "word"},
                {"data": "pval"},
                {"data": "corpval"},
                {"data": "overlap"}]});
    return;}

$(function() {
    $(document).on('change.bs.fileinput', '.fileinput', function(e) {
        var $this = $(this),
            $input = $this.find('input[type=file]'),
            $span = $this.find('.fileinput-filename');
        var numFiles = $input[0].files.length;
        for(var i = 0; i < numFiles; i++)
            var namey = $input[0].files[i].name
            if((namey.substr(namey.length-4) != ".tsv")&&(namey.substr(namey.length-4) != ".csv")&&(namey.substr(namey.length-4) != ".txt")){alert("You may only upload files with the following extensions:\n.tsv\n.csv\n.txt\nPlease select different files and try again");$('#removeFiles').trigger("click");return;}
            
        if($input[0].files !== undefined && $input[0].files.length > 1) {
            $span.addClass('dropdown').html('<a href="#" data-toggle="dropdown" class="dropdown-toggle">Multiple files selected <i class="caret"></i></a><ul class="dropdown-menu" role="menu"><li>' + $.map($input[0].files, function(val) { return val.name; }).join('</li><li>') + '</li></ul>');}
        if($input[0].files !== undefined && $input[0].files.length <= 10){
            $('#dbqs').html('<div id="DBquestionsCont" class="form-group container"><h3>Please answer the following questions about the database files:</h3>');
            for(var i = 0; i < numFiles; i++){
                var namey = $input[0].files[i].name
                $('#dbqs').append('<h4>For "'+namey+'":</h4>');
                $('#dbqs').append('<label class="control-label" for="header'+String(i)+'">Does this table have headers?</label>');
                $('#dbqs').append('<div class="radio-inline"><label><input type="radio" name="header'+String(i)+'" value="y" required>Yes</label></div>');
                $('#dbqs').append('<div class="radio-inline"> <label><input type="radio" name="header'+String(i)+'" value="n" required>No</label></div><br>');
                if(namey.substr(namey.length-4) == ".tsv"){ 
                    $('#dbqs').append('<label for="delimiter'+String(i)+'">What delimiter does this file use (for tab, type tab)?</label><input type="text" size="4" name="delimiter'+String(i)+'" value="tab" form="geneForm" readonly="readonly" required><br>');}
                else if(namey.substr(namey.length-4) == ".csv"){ 
                    $('#dbqs').append('<label for="delimiter'+String(i)+'">What delimiter does this file use (for tab, type tab)?</label><input type="text" size="4" name="delimiter'+String(i)+'" value="," form="geneForm" readonly="readonly" required><br>');}
                else{
                    $('#dbqs').append('<label for="delimiter'+String(i)+'">What delimiter does this file use (for tab, type tab)?</label><input type="text" size="4" form="geneForm" name="delimiter'+String(i)+'" required><br>');}
                $('#dbqs').append('<label for="geneCol'+String(i)+'">Which column has the gene identifiers (numbering start at 1)?</label><input type="text" size="4" name="geneCol'+String(i)+'" required><br>');
                $('#dbqs').append('<label for="desCols'+String(i)+'">Which columns have the gene descriptions? <h5><b>Listing instructions:</b></h5><ul><li>Column numbering starts at 1</li><li>Separate each number by a space</li><li>Write \'end\' after the last number to indicate the rest of the columns</li></ul></label><br><textarea rows="1" class="form-control" name="desCols'+String(i)+'" form="geneForm" required></textarea><br>');
            }}
        else if($input[0].files !== undefined && $input[0].files.length > 10){alert("You may not upload more than 10 files for use as a database.");$('#removeFiles').trigger("click");}
    });});
$(function() {$('#removeFiles').click(function(){$('#dbqs').html('');})});
$(function() {$("input[name='species']").change(function(){
    if($(this).val()=='other'){$('#fileSelector').removeClass("hidden")}
    else{$('#fileSelector').addClass("hidden")}})});
