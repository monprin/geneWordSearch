# This file contains the custom classes need for the operation of the 
# rest of the GeneWordSearch program.

# Written by Joe Jeffers

class WordFreq:
# Class for keeping the words and their frequencies together and 
# and some useful functions to outsource some work
	def __init__(self, word, freq):
	# Constructor
		self.word = word
		self.p = 0
		self.pCor = 0
		self.freq = freq
		self.total = 0
		self.genes = []
		
	def forHuman(self,genes=False):
	# Standard string output function for humans
		ans = 'Word: ' + self.word + '\n'
		ans += 'P-value: ' + str(self.p) + '\n'
		ans += 'Corrected P-value: ' + str(self.pCor) + '\n'
		ans += 'Overlap: ' + str(self.freq) + '/' + str(self.total) + '\n'
		if(genes):
			ans += 'Genes Appeared In: '
			for gene in self.genes[:-1]:
				ans += gene + ' '
			ans += self.genes[-1]
			ans += '\n'
		return ans
		
	def forRobot(self,genes=False):
	# Returns the string output for machine readable output (tsv)
		ans = self.word + '\t'
		ans += str(self.p) + '\t'
		ans += str(self.pCor) + '\t'
		ans += str(self.freq) + '\t'
		ans += str(self.total) + '\t'
		if(genes):
			for gene in self.genes[:-1]:
				ans += gene + '\t'
			ans += self.genes[-1]
		return ans
		
	def to_JSON(self,genes=False):
	# Creates a JSON-formatted string representing the word. 
		ans = '{'
		ans += '"word": "' + self.word + '",'
		ans += '"pval": "' + str(round(self.p,7)) + '",'
		ans += '"corpval": "' + str(round(self.pCor,7)) + '",'
		ans += '"overlap": "' + str(self.freq) + '/' + str(self.total) + '"'
		if(genes):
			ans += ', genesin: ['
			for gene in self.genes[:-1]:
				ans += gene + ','
			ans += self.genes[-1]
			ans += ']'
		return (ans + '}')
		
	def to_JSON_array(words):
	# Helper function to correctly wrap the JSON objects in to a JSON array
		wordsJSON = '['
		for word in words[:-1]:
			wordsJSON += word.to_JSON() + ','
		wordsJSON += words[-1].to_JSON() + ']'
		return wordsJSON
	 
	def robotHeaders(genes=False):
	# Returns the headers for machine readable output (tsv)
		ans = 'Word' + '\t' + 'Pval' + '\t' + 'CorPval' + '\t' + 'Ocurrances in Sample' + '\t' + 'Ocurrances in Database'
		if(genes):
			ans += '\t' + 'Genes Appeared In'
		return ans
		
	def increment(self):
	# Adds another tick to the word count
		self.freq += 1
		
	def addGene(self,gene):
	# Adds the gene to the list of represented genes
		self.genes.append(gene)
		
	def computeP(self,db,length,totWords):
	# Computes the p value using hypergeometric distribution
	# Also finds and assigns the total word count from the database
	# Word count database must be built by 'totalWordCounts' function
		from scipy.stats import hypergeom
		self.total = db[self.word]
		self.p = hypergeom.sf((self.freq-1),totWords,self.total,length)
		
	def pCorrect(self,tot,pos):
	# Computes the corrected P value using the Holm-Bonferroni method
		self.pCor = (self.p * (tot-pos))
		
class GeneNote:
	# Class for holding a gene and all of the words that anotate it for the database.
	def __init__(self, gene):
		self.gene = gene
		self.words = set()
		self.littleWords = set()
		self.links = set()
		
	def addWords(self,words):
	# Adds word to the list of associated words
		for word in words:
			self.words.add(word)
	
	def addLink(self,link):
	# Adds link to the list of associated links
		self.links.add(link)
	
	def demoteWords(self,wordSet):
		self.links = self.words & wordSet
		self.words = self.words - wordSet
	
	def __str__(self):
	# Method for implicit string conversion, usually for printing
		ans = self.gene + '\t'
		for word in self.words:
			ans += word + '\t'
		for link in self.links:
			ans += link + '\t'
		return ans + '\n'
