# Routing directions
# Written by Joseph Jeffers

import re
import os
import json
from werkzeug import secure_filename
from flask import request, render_template, jsonify, redirect, url_for
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
	# Retrieve and sanitize the input
	print(request.form)
	dbFiles = request.form['fStrings[]']
	print(len(dbFiles))
	return jsonify(result='[{"word": "File Uploaded"}]')
	genes = str(request.form['geneList'])
	probCutoff = float(request.form['probCut'])
	save(request.files['geneDBs'])
	genes = re.split('\r| |,|\t|\n',genes)
	genes = list(filter((lambda x: x != ''),genes))
	
	# Build up the tmp database
	#from genewordsearch import DBBuilder
	#DBBuilder.tempBuilder(genes)
	
	
