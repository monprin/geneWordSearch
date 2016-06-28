# Function to build the databases that are necessary for GeneWordSearch
# Written by Joseph Jeffers

import re
import os
import pickle
import shutil
from genewordsearch.Classes import GeneNote, WordFreq

def geneWordBuilder(species,infiles,geneCols,desCols,delimiters,headers):
# Function that makes the annotation database
#	species - str of the name of the species
#	infiles - the raw database file names
#	geneCols - list of numbers representing the column containing the gene IDs in the respective file
#	desCols - list of lists of strs containg the columns that have descriptions in them for the respective files
#	delimeters - list of strings containing the delimeters for the respective files
#	headers - list of booleans denoting whether or not the respective files have headers

	db = dict()

	#----------------Building the gene database---------------------
	fileNum = 0
	for infile in infiles:
	# For each of the given files, process all the genes present
		# Convert from human column numbering to computer numbering
		geneCol = int(geneCols[fileNum])-1
		desCol = desCols[fileNum].split(' ')
		if (desCol[-1] == 'end'):
			toEnd = True
			desCol = desCol[:-1]
		else:
			toEnd = False
		desCol = [int(x)-1 for x in desCol]
		maxDes = max(desCol)

		matrix = open(infile)
		rowNum = 0

		# Find Splitter
		if(delimiters[fileNum] == 'tab'):
			splitter = '\t'
		else:
			splitter = delimiters[fileNum]

		# Deal with headers
		if(headers[fileNum]):
			garb = matrix.readline()
			rowNum += 1
			del garb

		# Process file line by line, each line has different gene.
		skippedRows = []
		for line in matrix.readlines():
			# Get rid of newline char
			line = line[:-1]

			# Split into columns
			row = line.split(splitter)

			# Handle short lines in the database
			if(len(row)-1 <= maxDes):
				skippedRows.append(rowNum)
				rowNum += 1
				continue
			rowNum += 1

			# Get the gene name, free of any sublocus notation
			geneName = row[geneCol].lower()
			geneName = re.split('\.',geneName)
			geneName = geneName[0]

			# Add gene object to db if not there already
			if(geneName not in db):
				db[geneName] = GeneNote(geneName)

			# Getting the columns that have the descriptions
			desColTemp = desCol[:]
			if(toEnd):
				last = desColTemp[-1]
				desColTemp += list(range((last+1),len(row)))
			rowed = [row[x] for x in desColTemp]
			row = rowed
			del rowed
			del desColTemp
			words = []

			# Putting web links in their container if needed
			for entry in row:
				if(entry[:4] == 'http'):
					db[geneName].addLink(entry)
					row.remove(entry)

			# Splitting the words up by various delimiations
			db[geneName].addAnnotations(row)
			for entry in row:
				words += re.split(' |_|,|\.|/|\(|\)|\;|\:',entry.lower())

			# Get rid of the blank entries, and other useless stuff
			locPattern = 'loc.*'
			genePattern = '[a-z]{1,3}\d{1,2}g\d*'
			alphaNumPattern = '[a-z]{1,4}\d*'
			virgPattern = 'virgatum.*'
			f = lambda x: not((x == '-') or (x == None) or (x.isdigit())
			or (x == '') or (len(x) <= 1) or (re.fullmatch(locPattern,x))
			or (re.fullmatch(genePattern,x)) or (re.fullmatch(virgPattern,x))
			or (re.fullmatch(alphaNumPattern,x)))
			words = list(filter(f,words))

			# Add all of the words into the database
			db[geneName].addWords(words)
			fileNum += 1

		matrix.close()


	# Counting the words
	wordList = wordCounter(db)

	# Getting rid of little and big words
	x = littleWordRemover(db,wordList)

	# Bookeeping and saving files
	bookkeeper(species, x[0], x[1])

	return

def tempBuilder(genes,species):
# Function to build temporary database for running genes against smaller
#	genes - subset of all species genes
#	species - str of the species name to be saved under

	# Load the full DB to exatract items from
	dbFolder = os.getenv('GWS_STORE', '~/.gws/') + species.lower().replace(' ','')
	try:
		dbfile = open(dbFolder + '/geneNotes.p','rb')
	except:
		raise ValueError('There is no database associated with this species, please use either \'maize\' or \'ath\', or make your own using \'--buildDB\'.')
	fullDB = pickle.load(dbfile)
	db = dict()

	print('Finding the requested genes...')
	# Find all of the needed genes and add them to the new DB
	for gene in genes:
		name = gene.lower()
		try:
			db[name] = fullDB[name]
		except KeyError:
			print(name + ' is not in the full database')
	del fullDB

	print('Counting the words...')
	wordList = wordCounter(db)

	print('Getting rid of little and big words...')
	x = littleWordRemover(db,wordList)

	print('Bookeeping and saving files...')
	bookkeeper('tmp', x[0], x[1])
	print('Database built. See databases/tmp/ for the output.')
	return

def cleanTmp():
	# Function to clean up the temporary database files
	shutil.rmtree(os.getenv('GWS_STORE', '~/.gws/') + 'tmp')
	return

def wordCounter(db):
# Internal Method
# Takes in a database dictionary and returns sorted list of WordFreq objects
# sorted by how often they occur.

	#Make a list of all the words associated genes in the database
	words = []
	for gene in list(db.values()):
		words += gene.words

	# Sorting the words into alphabetical order
	words.sort()
	wordList = []

	# Counting the words
	for item in words:
		if(wordList == [] or wordList[0].word != item):
			wordList.insert(0, WordFreq(item,1))
		else:
			wordList[0].increment()
	del words

	# Sorting now by frequency instead of alphabetical and return it
	return sorted(wordList, key=lambda item: item.freq,reverse=True)

def littleWordRemover(db, wordListRaw, upper=10000, lower=3):
# Internal Method
# Find the too frequent and too infrequent words and purge them from the
# the gene database and the word frequency list

	remList = set()
	wordList = []
	for word in wordListRaw:
		freq = word.freq
		if((freq >= upper) or (freq <= lower)):
			remList.add(word.word)
		else:
			wordList.append(word)
	del wordListRaw

	# Demote them in the database
	for key in db:
		db[key].demoteWords(remList)
	return (db,wordList)

def bookkeeper(species, geneDB, countList):
# Internal Method
# Make all of the necessary files

	# Find the total word count, add it to the list
	total = 0
	for word in countList:
		total += word.freq
	countList.insert(0,WordFreq('Total Count',total))

	# Determine outfile locations
	dbFolder = os.getenv('GWS_STORE', '~/.gws/') + species.lower().replace(' ','')
	os.makedirs(dbFolder, exist_ok=True)

	# --------------Save the gene database files-------------------

	# Make a text version for posterity (and error checking)
	printList = list(geneDB.values())
	geneFile = open(dbFolder+'/geneNotes.tsv','w',newline='')
	for gene in printList:
		if not(gene.gene == ''):
			geneFile.write(str(gene))
	geneFile.close()

	# Pickle that stuff! (for geneWordSearch function)
	pickle.dump(geneDB,open(dbFolder+'/geneNotes.p','wb'))

	# ---------------Save the total word count files----------------

	# Make a text version for posterity (and error checking)
	countFile = open(dbFolder+'/totalWordCounts.tsv','w')
	for word in countList:
		countFile.write(str(word.freq) + '\t' + str(word.word) + '\n')
	countFile.close()

	# Pickle a dictionary of that stuff! (for geneWordSearch function)
	countDB = dict()
	for word in countList:
		countDB[word.word] = word.freq
	pickle.dump(countDB,open(dbFolder+'/totalWordCounts.p','wb'))

	return
# ---------------------Deprecated at the momment------------------------
def networksBuilder(infile,species):
# Creates dictionary for gene networks. Used by CLI for network finder

	sheet = open(infile)
	networks = {}

	# Dealing with headers
	sheet = open(infile)
	headers = input('Does this file have headers (y or n)? ')
	if(headers == 'y' or headers == 'Y'):
		headers == True
	elif(headers == 'n' or headers == 'N'):
		headers == False
	else:
		raise ValueError('Please indicate whether your data has headers using y or n.')
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
