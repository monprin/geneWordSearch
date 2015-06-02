# Routing directions
import re
from webapp import app
from flask import request
from src.Classes import WordFreq
from flask import render_template
from src.GeneWordSearch import geneWordSearch

@app.route('/',methods=['GET','POST'])
def home():
	if request.method == 'POST':
		genes = request.form['genes']
		species = request.form['species'].lower()
		genes = re.split('\n| |,',genes)
		results = geneWordSearch(genes,species)
		ans = '<p>' + WordFreq.robotHeaders(genes) + '</p>'
		for word in results[0]:
			ans += '<p>' + word.forRobot() + '</p>'
		return ans
	else:
		return render_template('home.html')
