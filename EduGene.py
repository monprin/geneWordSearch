# v0.3 Gene Word Cloud Program
# Joe Jeffers

def geneWordSearch(genes,webLinks=False,minChance=0.05,machineRead=False):
	# Input: Takes in a gene identifier and the built database from the above function.
	# Output: Prints out all the genes that have a chance probability of less than the minChance variable. 
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
	
	# Print the results that are above the chance threshold
	# machineRead Parameter prints the output as a tsv sheet to be used for a machine readable format
	if(machineRead):
		# Print the header for the table
		print(WordFreq.robotHeaders())
		
		# Print the lines using class function
		for item in wordList:
			if(item.p <= minChance):
				print(item.forRobot())
		
		if(webLinks):
			for link in webSites:
				print(link)
		
	else:
		for item in wordList:
			if(item.p <= minChance):
				print(item.forHuman())
		if(webLinks):
			print('Web Links associated with these genes:'+'\n')
			for link in webSites:
				print(link + '\n')

# Command Line interface:
if __name__ == '__main__':
	import sys
	import argparse
	parser = argparse.ArgumentParser(description='Find the important words associated with supplied genes.')
	parser.add_argument('-w',action='store_true',default=False,help='This will output associated weblinks with standard gene output.')
	parser.add_argument('-p',action='store',type=float,default=0.05,help='This option takes one argument and sets the probability cutoff, default is 0.2.')
	parser.add_argument('-m',action='store_true',default=False,help='This will give a tsv output for machine readable purposes. Default is human readable.')
	parser.add_argument('-f',action='store_true',default=False,help='This indicates that the input strings will be files with genes in them')
	parser.add_argument('-d',action='store_true',default=False,help='Indicates that the input is a directory and will process all files in the directory')
	parser.add_argument('things',action='store',nargs='*')
	args = parser.parse_args()
	if(args.f):
		genes = []
		for name in args.things:
			geneList = open(name)
			for row in geneList.readlines():
				genes += row.split()
			geneWordSearch(genes,webLinks=args.w,minChance=args.p,machineRead=args.m)
	
	
	elif(args.d):
		import glob
		
		for folder in args.things:
			if(not(folder[-1] == '/')):
				folder += '/'
			fileList = glob.glob(folder + '*.txt')
			for fileName in fileList:
				genes = []
				geneList = open(fileName)
				for row in geneList.readlines():
					genes += row.split()
				if((len(genes) >= 10) and (len(genes) <= 300)):
					print('\n')
					print('Results for ' + fileName + ':')
					print('\n')
					geneWordSearch(genes,webLinks=args.w,minChance=args.p,machineRead=args.m)
				geneList.close()
	
	else:
		genes = args.things
		geneWordSearch(genes,webLinks=args.w,minChance=args.p,machineRead=args.m)
	
