# Functions to find statistics about the databases
# Joe Jeffers
# 11/9/2014

# Function produces total word count file. Run to update as 
# needed, takes about 10 min to run on 2011 Core i5
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
	
	for row in db:
		listing = row[6:]
		for entry in listing:
		# Removing Web links, but keeping count
			if(entry[:4] == 'http'):
				links += 1
				listing.remove(entry)
		# Splitting the words up by various delimiations
		for entry in listing:	
			words += re.split(' |_|,|\.|/',entry)
				
	wordList = list(filter(None,words))

	# Building the infrastructure for counting the words
	freq = []
	word = []
	pval = []
	wordFreq = []
	
	# Adding the web link counts to the list
	freq.append(links)
	word.append('Web Links')
	
	# Counting the words while emptying the word list
	while not(wordList == []):
		item = wordList.pop()
		if(item in word):
			index = word.index(item)
			freq[index] += 1
		else:
			word.append(item)
			freq.append(1)
	
	# Putting the frequency list together with the word list
	i = 0
	while i < len(word):
		x = [freq[i],word[i]]
		wordFreq.append(x)
		i += 1
	
	wordFreq.sort(reverse=True)
	f = open('totalWordCount.txt', 'w')
	for line in wordFreq:
		f.write(str(line[0]) + '	' + str(line[1])+'\n')
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

