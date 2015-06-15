# Main logic function for finding the annotations associated with the genes.

# Written by Joe Jeffers

def geneWordSearch(genes,species,minChance=0.05,corrected=False):
# Input: Takes in a list of genes, the species, and the probability cutoff.
# Output: Returns tuple of words and links. Only returns the genes that have a 
#         chance probability of less than the minChance variable. 
	import re
	import pickle
	from genewordsearch.Classes import WordFreq
	from genewordsearch.Classes import GeneNote
	
	# Unpickle the database of words
	dbfile = open('databases/'+ species +'/geneNotes.p','rb')
	db = pickle.load(dbfile)
	
	# Build the word list up for all of the genes provided.
	words = []
	webSites = []
	links = WordFreq('Web Links',0)
	for item in genes:
		# Make the input all lowercase to match the database
		gene = item.lower()
		i=1
		
		# Get the object from the DB
		geneData = db[gene]
		
		# Adding words related to the gene in db to the overall list
		for word in geneData.words:
			words.append([word,geneData.gene])
		
		# Dealing with the websites
		for link in geneData.links:
			links.addGene(geneData.gene)
			webSites.append(link)

	# Sort to put words in alphabetical order for counting
	words.sort()
	
	# Adding the web link counts to the list
	wordList = []
	
	# Counting the words
	for item in words:
		if(wordList == [] or wordList[0].word != item[0]):
			wordList.insert(0, WordFreq(item[0],1))
			wordList[0].addGene(item[1])
		else:
			wordList[0].increment()
			wordList[0].addGene(item[1])
	del words
	
	# Getting rid of words that don't happen in enough genes to matter
	wordListRaw = wordList[:]
	wordList = []
	length = 0
	for word in wordListRaw:
		if(word.freq >= 3):
			wordList.append(word)
			length += word.freq
	del wordListRaw
	
	# Finding the respective P values
	pickleDict = open('databases/'+ species +'/totalWordCounts.p','rb')
	wordCounts = pickle.load(pickleDict)
	totalWords = wordCounts['Total Count']
	for word in wordList:
		word.computeP(wordCounts,length,totalWords)
	pickleDict.close()
	del wordCounts
	
	# Sorting now by P Value instead of alphabetical
	wordList = sorted(wordList, key=lambda item: item.p)
	
	# Finding corrected P Values using Holm–Bonferroni method
	count = len(wordList)
	for i in range(0,count):
		wordList[i].pCorrect(count,(i+1))
	
	# Sort by corrected P Value instead of original P value if desired
	if(corrected):
		wordList = sorted(wordList, key=lambda item: item.pCor)
	
	# Filtering out results that are higher than the minimum chance threshold
	wordList = filter(lambda x: x.p <= minChance,wordList)
	
	return (list(wordList),list(webSites))
