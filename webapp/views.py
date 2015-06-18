# Routing directions
# Written by Joseph Jeffers

import re

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
	import os
	import glob
	import shutil
	from genewordsearch.DBBuilder import geneWordBuilder 
	
	# Prep the database files for processing
	ip = str(request.environ['REMOTE_ADDR'])
	folder = os.path.join(app.config['UPLOAD_FOLDER'], ip)
	os.makedirs(folder, exist_ok=True)
	dbFiles = request.files.getlist('geneDBs')
	fileCount = len(dbFiles)
	fileNum = 0
	for db in dbFiles:
		filename = secure_filename(db.filename)
		db.save(os.path.join(folder, (str(fileNum)+filename[-4:])))
		fileNum += 1
	fileList = glob.glob(folder+'/*')
	fileList.sort()
	
	# Pull and organize the rest of the database info
	headers = []
	headtxt = []
	delimiters = []
	geneCols = []
	desCols = []
	fileNum = 0
	while(fileNum < fileCount):
		headtxt.append(str(request.form['header'+str(fileNum)]))
		delimiters.append(str(request.form['delimiter'+str(fileNum)]))
		geneCols.append(str(request.form['geneCol'+str(fileNum)]))
		desCols.append(str(request.form['desCols'+str(fileNum)]))
		fileNum += 1
	for header in headtxt:
		if(header =='y'):
			headers.append(True)
		else:
			headers.append(False)
	geneWordBuilder(ip,fileList,geneCols,desCols,delimiters,headers)
	shutil.rmtree(folder+'/')
	
	# Run the enrichment analysis
	genes = str(request.form['geneList'])
	probCutoff = float(request.form['probCut'])
	genes = re.split('\r| |,|\t|\n',genes)
	genes = list(filter((lambda x: x != ''),genes))
	results = geneWordSearch(genes,ip,minChance=probCutoff)
	ans = WordFreq.to_JSON_array(results[0])
	shutil.rmtree('databases/'+ip+'/')
	return jsonify(result=ans)
	
	
