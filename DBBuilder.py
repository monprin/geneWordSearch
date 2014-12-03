# Function to build the gene annotation database and pickle it

class GeneNote:
	# Class for holding a gene and all of the words that anotate it.
	def __init__(self, gene):
		self.gene = gene
		self.words = []
		self.links = []
		
	def addWord(self,word):
		self.words.append(word)
		
	def addLink(self,link):
		self.links.append(link)
		
	def toString(self):
		ans = self.gene + '\t'
		for word in self.words[:-1]:
			ans += word + '\t'
		if(self.links == [] and not(self.words == [])):
			ans += self.words[-1]
			return ans + '\n'
		for link in self.links[:-1]:
			ans += link + '\t'
		if not(self.links == []):
			ans += self.links[-1]
		return ans + '\n'
			
		
def geneWordBuilder(infile='databases/geneMatrix.txt',outfile='databases/geneNotes.txt'):
	import re
	import pickle
	
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
			fin.write(gene.toString())
	fin.close()
	
	# Pickle that stuff! (for geneWordSearch function)
	pickle.dump(NoteDB,open('databases/geneNotes.p','wb'))
	
	return