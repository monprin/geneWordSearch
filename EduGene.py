# v0.2 Gene Word Cloud Program
# Joe Jeffers

class WordFreq:
	# Class for keeping the words and their frequencies together and 
	# and some useful functions to outsource some work
	def __init__(self, word, freq):
		self.word = word
		self.p = 0
		self.freq = freq
		self.total = 0
		self.genes = []
		
	def forHuman(self):
		# Standard string output function
		ans = 'Word: ' + self.word + '\n'
		ans += 'P-value: ' + str(self.p) + '\n'
		ans += 'Overlap: ' + str(self.freq) + '/' + str(self.total) + '\n'
		ans += 'Genes Appeared In: '
		for gene in self.genes:
			ans += gene + ' '
		ans += '\n'
		return ans
		
	def forRobot(self):
		# Returns the string output for machine readable tsv.
		ans = self.word + '\t'
		ans += str(self.p) + '\t'
		ans += str(self.freq) + '\t'
		ans += str(self.total) + '\t'
		for gene in self.genes[:-1]:
			ans += gene + '\t'
		ans += self.genes[-1]
		return ans
		
	def robotHeaders():
		# Returns the headers for machine readable output
		return 'Word' + '\t' + 'Pval' + '\t' + 'Ocurrances in Sample' + '\t' + 'Ocurrances in Database' + '\t' + 'Genes Appeared In'
		
	def increment(self):
		# Adds another tick to the word count
		self.freq += 1
		
	def addGene(self,gene):
		# Adds the gene to the list of represented genes
		self.genes.append(gene)
		
	def computeP(self,db,length):
		# Computes the p value using hypergeometric distribution
		# Also finds and assigns the total word count from the database
		from scipy.stats import hypergeom
		for line in db:
			if(line[1] == self.word):
				self.total = int(line[0])
				break
		self.p = hypergeom.sf(self.freq,1398197,self.total,length)
		

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
		
	x.close()
	return db
	
def wordCountDBMaker():
	# Much like the above function, pulls in database file for total 
	# word counts and returns a 2 by n array. 
	x = open('totalWordCount.txt')
	db = []
	
	for line in x.readlines():
		row = line.split('\t')
		row[1] = row[1][:len(row[1])-1]
		row[0] = int(row[0])
		db.append(row)
		
	x.close()	
	return db

def geneWordSearch(genes,webLinks=False,minChance=0.05,machineRead=False):
	# Input: Takes in a gene identifier and the built database from the above function.
	# Output: Prints out all the genes that have a chance probability of less than the minChance variable. 
	import re
	
	
	db = geneDBMaker()
	
	words = []
	links = 0
	webSites = []
	# Build the word list up for all of the genes provided.
	links = WordFreq('Web Links',0)
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
		# Removing Web links, but keeping count
		
		for entry in listing:
			if(entry[:4] == 'http'):
				links.increment()
				links.addGene(gene)
				webSites.append(entry)
				listing.remove(entry)	
		# Splitting the various strings into individual words per list item
		adj = []
		for entry in listing:
			adj += re.split(' |_|,|\.',entry)	
		adj= list(filter(None,adj))
		
		for entry in adj:
			words.append([entry,gene])

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
	wordCounts = wordCountDBMaker()
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
	parser.add_argument('genes',action='store',nargs='*')
	args = parser.parse_args()
	geneWordSearch(args.genes,webLinks=args.w,minChance=args.p,machineRead=args.m)
