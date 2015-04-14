# Function to build the various needed databases for this function
# These functions will be generalized to be able to make databases for any input
# but that is for a future versaion, included now for reference.

# Written by Joseph Jeffers
# Updated Jan 12 2015

def geneWordBuilder(infiles,species):
# Function that makes the annotation database
	import re
	import pickle
	from Classes import GeneNote
	
	db = dict()
	
	for infile in infiles:
		print('For file \'' + infile + '\', please answer the following questions:')
		geneCol = input('What column contains the gene identifiers (numbered from 1)? ')
		desCol = input('What columns contain the description fields (please type each number seperated by a space)? ')
		
		# Convert from human column numbering to computer column numbering
		geneCol = int(geneCol)-1
		desCol = desCol.split(' ')
		desCol = [int(x)-1 for x in desCol]
		maxDes = max(desCol)
		
		matrix = open(infile)
		
		# Figure out the file type
		if(infile[-3:] == 'tsv'):
			splitter = '\t'
		elif(infile[-3:] == 'csv'):
			splitter = ','
		else:
			splitter = input('Please type the charachter used to seperate columns in this document (tab = \t, rest are just the charachter): ')
		
		# Dealing with headers
		headers = input('Does this file have headers (y or n)? ')
		if(headers == 'y' or headers == 'Y'):
			headers == True
		elif(headers == 'n' or headers == 'N'):
			headers == False
		else:
			raise ValueError('Please indicate whether your data has headers using y or n.')
		if(headers):
			garb = matrix.readline()
			del garb
		
		# Process file line by line, each line has different gene.
		skippedRows = 0
		for line in matrix.readlines():
			# Get rid of newline char, make fully lowercase, and split into columns
			line = line[:-1]
			row = line.split(splitter)
			
			# Handle short lines in the database
			if(len(row) <= maxDes):
				skippedRows += 1
				continue
			
			# Get the gene name, free of any sublocus notation
			geneName = row[geneCol].lower()
			geneName = re.split('\.',geneName)
			geneName = geneName[0]
			
			# Add Gene Object to db if not there already
			if(geneName not in db):
				db[geneName] = GeneNote(geneName)
			
			# Getting the columns that have the descriptions
			rowed = [row[x] for x in desCol]
			row = rowed
			del rowed
			words = []
			
			# Putting weblinks in their container if needed
			for entry in row:
				if(entry[:4] == 'http'):
					db[geneName].addLink(entry)
					row.remove(entry)
			
			# Splitting the words up by various delimiations
			for entry in row:
				words += re.split(' |_|,|\.|/|\(|\)|\;|\:',entry.lower())
			
			# Get rid of the blank entries, and other useless stuff
			f = lambda x: not((x == '-') or (x == None) or (x.isdigit()) or (x == '') or (len(x) <= 1))
			words = list(filter(f,words))
			
			# Add all of the words into the database
			db[geneName].addWords(words)
			
		matrix.close()
		
		print('Number of rows skipped due to different formatting: ' + str(skippedRows))
		print()
		
	# Determine outfile locations
	species = species.lower()
	folder = 'databases/' + species + '/'
	
	# Make a text version for posterity (and error checking)
	printList = list(db.values())
	fin = open(folder+'geneNotes.tsv','w',newline='')
	for gene in printList:
		if not(gene.gene == ''):
			fin.write(str(gene))
	fin.close()
	
	# Pickle that stuff! (for geneWordSearch function)
	pickle.dump(db,open(folder+'geneNotes.p','wb'))
	
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
# Answer: There are 989,373 words in the database as it is split and counted now.

# Just run it from the command line to rebuild and count everything.
import argparse
parser = argparse.ArgumentParser(description='Build the database for geneWordSearch.')
parser.add_argument('-s',action='store',type=str,default='ath',help='Define which species. Maize = maize, Arabidopsis = ath, or any other.')
parser.add_argument('files',action='store',nargs='*')
args = parser.parse_args()

print('Building Database...')
geneWordBuilder(args.files,args.s)
print('Done')
#print('Counting Word Instances...')
#totalWordCounts()
#print('Done')
#print('Total Words in the Database:')
#print(numOfWords())
