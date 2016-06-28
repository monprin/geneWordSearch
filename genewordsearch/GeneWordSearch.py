# Main logic function for finding the annotations associated with the genes.

# Written by Joe Jeffers

import re
import os
import pickle
from genewordsearch.Classes import WordFreq
from genewordsearch.Classes import GeneNote

def geneWordSearch(genes,species,minChance=0.05,minWordFreq=3,corrected=False):
# Does the analysis work of making of looking at the genes and doing the statistics
#	genes - list of strings of the gene ids in the set to be analysed
#	species - str of the species these genes belong to
#	minChance - the minimum probability that is acceptable for the word to be included in the Results
#	minWordFreq - the minimum amount of genes the word must appear in in the set to be counted
#	corrected - boolean saying whether the results should be cutoff using the corrected p value or the
#	            original p, if true, results are more reliable, but less numerous

	# Unpickle the database of words
	dbFolder = os.getenv('GWS_STORE', '~/.gws/') + species.lower().replace(' ','')
	try:
		dbfile = open(dbFolder + '/geneNotes.p','rb')
	except:
		raise ValueError('There is no database associated with '+species+', please use either \'maize\' or \'ath\', or make your own using \'--buildDB\'.')
	db = pickle.load(dbfile)

	# Build the word list up for all of the genes provided.
	words = []
	webSites = []
	badGenes = []
	links = WordFreq('Web Links',0)
	for item in genes:
		# Make the input all lowercase to match the database
		gene = item.lower()
		i=1

		# Get the object from the DB, skip term if it is not there
		try:
			geneData = db[gene]
		except KeyError:
			badGenes.append(gene)
			continue

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
		if(word.freq >= minWordFreq):
			wordList.append(word)
			length += word.freq
	del wordListRaw

	# Finding the respective P values
	pickleDict = dbfile = open(dbFolder + '/totalWordCounts.p','rb')
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

# Pull all annotation words for a list of genes
def geneWords(genes, species, raw=False):
	# Unpickle the database of words
	dbFolder = os.getenv('GWS_STORE', '~/.gws/') + species.lower().replace(' ','')
	try:
		dbFile = open(dbFolder + '/geneNotes.p','rb')
	except:
		raise ValueError('There is no database associated with \''+species+'\', please use either \'maize\' or \'ath\', or make your own using \'--buildDB\'.')
	db = pickle.load(dbFile)

	# Get terms from DB if present, otherwise just make it an empty list
	words = {}
	for gene in genes:
		try:
			if(raw):
				words[gene] = list(db[gene.lower()].annotations)
			else:
				words[gene] = list(db[gene.lower()].words)
		except KeyError:
			words[gene] = []
			continue

	return words
