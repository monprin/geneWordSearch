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

def geneWordSearch(gene,db):
	# Input: Takes in a gene identifier and the built database from the above function.
	# Output: A list of seperated words from the descriptions of the genes in the database file provided, also gets rid of web links.
	import re
	
	i=1
	while i<len(db):
		if db[i][0] == gene:
			break
		i += 1
	
	# Check to see if the entry was actually found or just ran out of entries
	if i >= len(db):
		raise ValueError('This gene is not in the supplied database')
		return
		
	listing = db[i]
	links = 0
	listing = listing[6:]
	words = []
	# Removing Web links, but keeping count
	for entry in listing:
		if(entry[:4] == 'http'):
			links += 1
			listing.remove(entry)	
	# Splitting the various strings into individual words per list item
	for entry in listing:
		words += re.split(' |-|_|,|\.',entry)	
	wordList = list(filter(None,words))

	# Building the infrastructure for counting the words
	freq = []
	word = []
	pval = []
	wordFreq = []
	
	# Adding the web link counts to the list
	freq.append(links)
	word.append('Web Links')
	
	# Counting the words while emptying the word list
	while not(wordList == []):
		item = wordList.pop()
		if(item in word):
			index = word.index(item)
			freq[index] += 1
		else:
			word.append(item)
			freq.append(1)
	
	# Putting the frequency list together with the word list
	i = 0
	while i < len(word):
		x = [freq[i],word[i]]
		wordFreq.append(x)
		i += 1
	
	wordFreq.sort(reverse=True)
	return wordFreq
	
def genePrinter(*args):
	# Wrapper for above functions to handle indefinite arguments and prints each out. 
	# Thoughts on what kind of output would be best besides just printing into the terminal?
	
	db = geneDBMaker()
	
	# Making all input lower case
	genes = []
	for arg in args:
		genes.append(arg.lower())
	
	for gene in genes:
		listicle = geneWordSearch(gene,db)
		print(gene)
		print(listicle)
		
	
	
	
	
	
