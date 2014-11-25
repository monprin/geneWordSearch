# Functions to find statistics about the databases
# Joe Jeffers
# 11/9/2014

# Function produces total word count file. Run to update as 
# needed, takes about 10 min to run on 2011 Core i5

class WordFreq:
	# Class for keeping the words and their frequencies together
	def __init__(self, word, freq):
		self.word = word
		self.freq = freq
	def increment(self):
		self.freq += 1

def totalWordCounts():
	import re
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
	
	links = 0
	words = []
	genelist = []
	
	for row in db:
		gene = row[0]
		listing = row[6:]
		for entry in listing:
		# Removing Web links, but keeping count
			if(entry[:4] == 'http'):
				links += 1
				listing.remove(entry)
		# Splitting the words up by various delimiations
		for entry in listing:	
			words += re.split(' |_|,|\.|/',entry)
				
	# Get rid of the blank entries
	words = list(filter(None,words))
	
	# Sort to put all the same words together
	words.sort()
	
	# Counting the consecutive words, no membership check makes this fairly fast
	wordFreq = []
	wordFreq.append(WordFreq('Web Links',links))
	for item in words:
		if(wordFreq[0].word != item):
			wordFreq.insert(0, WordFreq(item,1))
		else:
			wordFreq[0].increment()
	del words
	
	# Sorting now by frequency instead of alphabetical
	wordFreq = sorted(wordFreq, key=lambda item: item.freq, reverse=True)
	
	# Printing in the proper format to the file
	f = open('totalWordCount.txt', 'w')
	for line in wordFreq:
			f.write(str(line.freq) + '	' + str(line.word) + '\n')
	f.close()
	return

# Returns the total word count of the entire database using the totalWordCount.txt
def numOfWords():
	x = open('totalWordCount.txt')
	sum = 0;
	
	for line in x.readlines():
		row = line.split()
		sum += int(row[0])
		
	return sum
# Answer: There are 1,398,197 words in the database	as it is split and counted now.

