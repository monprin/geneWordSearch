# Main logic function for finding the annotations associated with the genes.

# Written by Joe Jeffers
# Updated on Jan 12 2015

def geneWordSearch(genes,minChance=0.05):
	# Input: Takes in a list of genes and the probability cutoff.
	# Output: Returns tuple of words and links. Only returns the genes that have a 
	# chance probability of less than the minChance variable. 
	import re
	import pickle
	from Classes import WordFreq
	from Classes import GeneNote
	
	# Unpickle the database of words
	dbfile = open('databases/geneNotes.p','rb')
	db = pickle.load(dbfile)
	
	words = []
	webSites = []
	x = len(db)
	# Build the word list up for all of the genes provided.
	links = WordFreq('Web Links',0)
	for item in genes:
		# Make the input all lowercase to match the database
		gene = item.lower()
		i=1
		
		# Find the right gene
		
		while i<x:
			if db[i].gene == gene:
				break
			i += 1
		
		# Check to see if the entry was actually found or just ran out of entries
		if i >= x:
			raise ValueError('Gene: ' + gene + ' is not in the supplied database')
			return
		geneData = db[i]
		# Adding words related to the gene in db to the overall list
		for word in geneData.words:
			words.append([word,geneData.gene])
		
		# Dealing with the websites
		for link in geneData.links:
			links.addGene(geneData.gene)
			webSites.append(link)

	# Sort to put words in alphabetical order for counting
	words.sort()
	length = len(words)
	
	# Adding the web link counts to the list
	wordList = []
	wordList.append(links)
	
	# Counting the words
	for item in words:
		if(wordList == [] or wordList[0].word != item[0]):
			wordList.insert(0, WordFreq(item[0],1))
			wordList[0].addGene(item[1])
		else:
			wordList[0].increment()
			if(item[1] not in wordList[0].genes):
				wordList[0].addGene(item[1])
	del words
	
	# Finding the respective P values
	pickleDict = open('databases/totalWordCounts.p','rb')
	wordCounts = pickle.load(pickleDict)
	for word in wordList:
		word.computeP(wordCounts,length)
	del wordCounts
	
	# Sorting now by frequency instead of alphabetical
	wordList = sorted(wordList, key=lambda item: item.p)
	
	# Filtering out results that are higher than the minimum chance threshold
	wordList = filter(lambda x: x.p <= minChance,wordList)
	
	return (wordList,webSites)
