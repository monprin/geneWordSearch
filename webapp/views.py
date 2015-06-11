# Routing directions
import re
from flask import request
from flask import render_template
from webapp import app
from genewordsearch.Classes import WordFreq
from genewordsearch.GeneWordSearch import geneWordSearch

@app.route('/',methods=['GET','POST'])
def home():
	if request.method == 'POST':
		genes = request.form['genes']
		species = request.form['species'].lower()
		genes = re.split('\r| |,|\t|\n',genes)
		genes = list(filter((lambda x: x != ''),genes))
		print(genes)
		#ans = ''
		#for gene in genes:
		#	ans += gene + '\n'
		results = geneWordSearch(genes,species)
		ans = '<p>' + WordFreq.robotHeaders(genes) + '</p>'
		for word in results[0]:
			ans += '<p>' + word.forRobot() + '</p>'
		return ans
	else:
		return render_template('home.html')
