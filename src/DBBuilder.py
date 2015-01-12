# Function to build the various needed databases for this function
# These functions will be generalized to be able to make databases for any input
# but that is for a future versaion, included now for reference.

# Written by Joseph Jeffers
# Updated Jan 12 2015

def geneWordBuilder(infile,outfile='databases/geneNotes.tsv',headers=True):
# Function that makes the annotation database
	import re
	import pickle
	from Classes import GeneNote
	
	matrix = open(infile)
	db = []
	NoteDB = []
	
	# Get rid of headers if so indicated
	if(headers):
		garb = matrix.readline()
		del garb
	
	# Process file line by line, each line has different gene.
	for line in matrix.readlines():
		row = line.split('\t')
		# This section needed to remove the newline charachter off each
		# new line read from the file
		lastCol = len(row)-1
		row[lastCol] = row[lastCol][:len(row[lastCol])-1]
		# Adds list representing row as a new item to the database list
		db.append(row)
		
	matrix.close()
	
	for row in db:
		words = []
		NoteDB.append(GeneNote(row[0]))
		listing = row[6:]
		
		# Putting weblinks in their container
		for entry in listing:
			if(entry[:4] == 'http'):
				NoteDB[-1].addLink(entry)
				listing.remove(entry)
		# Splitting the words up by various delimiations
		for entry in listing:	
			words += re.split(' |_|,|\.|/',entry)
		
		# Get rid of the blank entries
		words = list(filter(None,words))
		
		# Add all of the words in the 
		for word in words:
			NoteDB[-1].addWord(word)
	
	# Make a text version for posterity?
	fin = open(outfile,'w',newline='')
	for gene in NoteDB:
		if not(gene.gene == ''):
			fin.write(str(gene))
	fin.close()
	
	# Pickle that stuff! (for geneWordSearch function)
	pickle.dump(NoteDB,open('databases/geneNotes.p','wb'))
	
	return
	
def totalWordCounts():
# Creates the dictionary of word occurances for use in geneWordSearch
	import pickle
	from Classes import WordFreq
	from Classes import GeneNote
	
	# Unpickle the database of words
	dbfile = open('databases/geneNotes.p','rb')
	db = pickle.load(dbfile)
	
	# Make a list of all the words associated genes in the database
	words = []
	links = []
	for gene in db:
		words += gene.words
		links += gene.links
	
	# Sorting the words into alphabetical order
	words.sort()

	# Counting the words
	wordList = []
	wordList.append(WordFreq('Web Links',len(links)))
	del links
	for item in words:
		if(wordList == [] or wordList[0].word != item):
			wordList.insert(0, WordFreq(item,1))
		else:
			wordList[0].increment()
	del words
	
	# Sorting now by frequency instead of alphabetical
	wordList = sorted(wordList, key=lambda item: item.freq,reverse=True)
	
	# Building the dictionary of the words
	dictDB = dict()
	for word in wordList:
		dictDB[word.word] = word.freq
		
	# Print file
	totalsFile = open('databases/totalWordCounts.tsv','w')
	for word in wordList:
		totalsFile.write(str(word.freq) + '\t' + str(word.word) + '\n')
	totalsFile.close()
	
	# Pickle the dictionary
	pickle.dump(dictDB,open('databases/totalWordCounts.p','wb'))
	
	
def networksBuilder(infile,outfile='databases/networks',headers=True):
# Creates dictionary for gene networks. Used by CLI for network finder
	import pickle
	
	sheet = open(infile)
	networks = {}
	
	# Get rid of headers if indicated
	if(headers):
		garb = sheet.readline()
		del garb
	
	gene = ''
	related = []
	
	# Each line of the data file is gone through, and it is presumed to be in order.
	for line in sheet.readlines():
		relation = line.split()
		relation = relation[:2]
		if(relation[0] == gene):
			# Building up gene relation list
			related.append(relation[1])
		elif(gene == ''):
			# Special Case for first entry
			gene = relation[0]
			related.append(relation[1])
		else:
			# Add list to Dictionary
			networks[gene] = related
			# Clearign variables
			gene = ''
			related = []
			# Starting new gene for listing
			gene = relation[0]
			related.append(relation[1])
			
	# Pickle the dictionary
	pic = outfile + '.p'
	pickle.dump(networks,open(pic,'wb'))
	
	# Print file
	tex = outfile + '.txt'
	networkFile = open(tex,'w')
	while(True):
		try:
			thing = networks.popitem()
		except KeyError:
			break
		networkFile.write(thing[0] + '\t' + str(thing[1]) + '\n')
	networkFile.close()

	
# Returns the total word count of the entire database using the totalWordCount.txt
def numOfWords():
	x = open('databases/totalWordCounts.tsv')
	sum = 0;
	
	for line in x.readlines():
		row = line.split()
		sum += int(row[0])
		
	return sum
# Answer: There are 1,398,154 words in the database	as it is split and counted now.

