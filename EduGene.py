# v0.1 Gene Word Cloud Program
# Joe Jeffers
# Updated 10/21/2014

def geneDBMaker():	
	# Takes in tab separated text file containing genetic relation data 
	# outputs this data in the form of a Python list of Python lists
	import fileinput
	
	x = open('geneMatrix.txt')
	db = []

	for line in x.readlines():
		row = line.split('\t')
		# This section needed to remove the newline charachter off each
		# new line read from the file
		lastCol = len(row)-1
		row[lastCol] = row[lastCol][:len(row[lastCol])-1]
		# Adds list representing row as a new item to the database list
		db.append(row)
		
	return db
	
def wordCountDBMaker():
	x = open('totalWordCount.txt')
	db = []
	
	for line in x.readlines():
		row = line.split('\t')
		row[1] = row[1][:len(row[1])-1]
		row[0] = int(row[0])
		db.append(row)
		
	x.close()	
	return db

def geneWordSearch(*genes,minChance=0.2):
	# Input: Takes in a gene identifier and the built database from the above function.
	# Output: The counts of words in the description ordered by frequency, also gets rid of web links.
	import re
	from scipy.stats import hypergeom
	
	db = geneDBMaker()
	
	wordList = []
	links = 0
	for item in genes:
		gene = item.lower()
		i=1
		while i<len(db):
			if db[i][0] == gene:
				break
			i += 1
	
		# Check to see if the entry was actually found or just ran out of entries
		if i >= len(db):
			raise ValueError('Gene: ' + gene + ' is not in the supplied database')
			return
		
		listing = db[i][6:]
		words = []
		# Removing Web links, but keeping count
		for entry in listing:
			if(entry[:4] == 'http'):
				links += 1
				listing.remove(entry)	
		# Splitting the various strings into individual words per list item
		for entry in listing:
			words += re.split(' |_|,|\.',entry)	
		wordList += list(filter(None,words))

	# Building the infrastructure for counting the words
	freq = []
	word = []
	pval = []
	wordFreq = []
	
	# Adding the web link counts to the list
	freq.append(links)
	word.append('Web Links')
	
	# Counting the words while emptying the word list
	length = int(len(wordList))
	while not(wordList == []):
		item = wordList.pop()
		if(item in word):
			index = word.index(item)
			freq[index] += 1
		else:
			word.append(item)
			freq.append(1)
	
	# Finding the respective P values
	i = 0
	wordCounts = wordCountDBMaker()
	while i < len(word):
		tot = 0
		for line in wordCounts:
			if(line[1] == word[i]):
				tot = int(line[0])
				break
		val = hypergeom.sf(int(freq[i]),1398197,tot,length)
		pval.append(val)
		i += 1
	del wordCounts
	
	# Putting the frequency list together with the word list
	i = 0
	while i < len(word):
		x = [pval[i],word[i],freq[i]]
		wordFreq.append(x)
		i += 1
	
	wordFreq.sort(reverse=False)
	for item in wordFreq:
		if(item[0] <= minChance):
			print(item)
