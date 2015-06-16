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

@app.route('/_gene_analysis', methods=['POST'])
def gene_analysis():
# Run the genes through genewordsearch
	# Sanitize the input
	species = str(request.form['species'])
	genes = str(request.form['geneList'])
	probCutoff = float(request.form['probCut'])
	genes = re.split('\r| |,|\t|\n',genes)
	genes = list(filter((lambda x: x != ''),genes))
	
	# Run the analysis and return the JSONified results
	results = geneWordSearch(genes,species,minChance=probCutoff)
	ans = WordFreq.to_JSON_array(results[0])
	return jsonify(result=ans)

@app.route('/_custom_db_analysis',methods=['POST'])
def custom_db_analysis():
# Deal with a custom database file
	# Sanitize the input
	genes = str(request.form['geneList'])
	probCutoff = float(request.form['probCut'])
	genes = re.split('\r| |,|\t|\n',genes)
	genes = list(filter((lambda x: x != ''),genes))
	
	# Build up the tmp database
	#from genewordsearch import DBBuilder
	#DBBuilder.tempBuilder(genes)
	return 'Not yet...'
