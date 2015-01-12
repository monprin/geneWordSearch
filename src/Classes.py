# File contains the custom classes need for the operation of the program.

# Written by Joe Jeffers
# Updated Jan 12 2015

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
		# Word count database must be dictionary with 'word' as the key, and count as value
		from scipy.stats import hypergeom
		self.total = db[self.word]
		self.p = hypergeom.sf((self.freq-1),1398197,self.total,length)
		
class GeneNote:
	# Class for holding a gene and all of the words that anotate it for the database.
	def __init__(self, gene):
		self.gene = gene
		self.words = []
		self.links = []
		
	def addWord(self,word):
	# Adds word to the list of associated words
		self.words.append(word)
		
	def addLink(self,link):
	# Adds link to the list of associated links
		self.links.append(link)
		
	def __str__(self):
	# Method for implicit string conversion, usually for printing
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
