# Routing directions
# Written by Joseph Jeffers

import re
import json
from flask import request, render_template, jsonify
from webapp import app
from genewordsearch.Classes import WordFreq
from genewordsearch.GeneWordSearch import geneWordSearch

@app.route('/')
def home():
# Base home page
	return render_template('home.html')

@app.route('/_gene_analysis')
def gene_analysis():
# Run the genes through genewordsearch
	# Sanitize the input
	species = str(request.args.get('species'))
	genes = str(request.args.get('genes'))
	genes = re.split('\r| |,|\t|\n',genes)
	genes = list(filter((lambda x: x != ''),genes))
	
	# Run the analysis and return the JSONified results
	results = geneWordSearch(genes,species)
	x = WordFreq.to_JSON_array(results[0])
	return jsonify(result=x)
