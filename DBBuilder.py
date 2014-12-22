# Function to build the gene annotation database and pickle it

def geneWordBuilder(infile='databases/geneMatrix.txt',outfile='databases/geneNotes.txt'):
	import re
	import pickle
	from Classes import GeneNote
	
	matrix = open(infile)
	db = []
	NoteDB = []
	
	# Get rid of headers
	garb = matrix.readline()
	del garb
	
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
