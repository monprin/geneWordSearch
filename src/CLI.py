# This is the Command Line interface for geneWordSearch.
# Needs to be run from the main program folder.

# Written by Joe Jeffers 
# Updated Jan 12 2015

from GeneWordSearch import geneWordSearch
import sys
import pickle
import argparse
from Classes import WordFreq

# Function to print the results 
def resultsPrinter(results, web, table, outfile):
	# Input: 
	#	The results from the geneWordSearch function
	#	a boolean for wheather to print links
	#	A boolean for whether it should be table output
	#	A writeable file object
	
	# Split the results
	words = results[0]
	links = results[1]
	
	if(table):
		# Print the header for the table
		outfile.write(WordFreq.robotHeaders()+ '\n')
	
		# Print the lines using class function
		for item in words:
			outfile.write(item.forRobot() + '\n')
	
	# Prints out web links if needed
		if(args.w):
			for link in links:
				outfile.write(link + '\n')
	
	else:
	# Prints out human readable for all the words.
		for item in words:
			outfile.write(item.forHuman() + '\n')
	
	# Prints out web links if needed
		if(args.w):
			outfile.write('Web Links associated with these genes:'+'\n' + '\n')
			for link in links:
				outfile.write(link + '\n' + '\n')

# Setup the Parser
parser = argparse.ArgumentParser(description='Find the important words associated with supplied genes.')
parser.add_argument('-d',action='store_true',default=False,help='Indicates that the input is a directory and will process all files in the directory. (Incompatible with -f and -n)')
parser.add_argument('-f',action='store_true',default=False,help='This indicates that the input strings will be a file with genes in it. (Incompatible with -d and -n)')
parser.add_argument('-n',action='store_true',default=False,help='Indicates that the input is the starting point of a network, will first return list of genes in those networks, then the traditional output on that list of genes. (Incompatible with -d and -f)')
parser.add_argument('-o',action='store',type=str,default='out.txt',help='Location to write the file that contains the results, default is out.txt in current folder.')
parser.add_argument('-p',action='store',type=float,default=0.05,help='This option takes one argument and sets the probability cutoff, default is 0.2.')
parser.add_argument('-t',action='store_true',default=False,help='This will give a tsv output for machine readable purposes. Default is human readable output.')
parser.add_argument('-w',action='store_true',default=False,help='This will output associated weblinks with standard gene output.')
parser.add_argument('things',action='store',nargs='*')

# Parse the arguments
args = parser.parse_args()

# Open the output file for writing
out = open(args.o,'w')

if(args.f):
# Deals with input if it is a file name
	genes = []
	for name in args.things:
		geneList = open(name)
		for row in geneList.readlines():
			genes += row.split()
	results = geneWordSearch(genes,minChance=args.p)
	resultsPrinter(results,args.w,args.t,out)

elif(args.n):
# Deals with finding the gene network
	genes = []
	nets = open('databases/networks.p','rb')
	networks = pickle.load(nets)
	
	for gene in args.things:
		genes += networks[gene]
	
	out.write('These are the genes related to the gene(s) you identified:'+'\n')	
	for gene in genes:
		out.write(gene + '\n')
	
	out.write('\n' + 'Results from this list:' + '\n' + '\n')
	results = geneWordSearch(genes,minChance=args.p)
	resultsPrinter(results,args.w,args.t,out)

elif(args.d):
# Deals with directory option
	import glob
	
	results = []
	for folder in args.things:
		if(not(folder[-1] == '/')):
			folder += '/'
		fileList = glob.glob(folder + '*.txt')
		for fileName in fileList:
			genes = []
			geneList = open(fileName)
			for row in geneList.readlines():
				genes += row.split()
			if((len(genes) >= 10) and (len(genes) <= 300)):
				out.write('\n' + '\n')
				out.write('Results for ' + fileName + ':')
				out.write('\n' + '\n')
				results = (geneWordSearch(genes,minChance=args.p))
				resultsPrinter(results,args.w,args.t,out)
			geneList.close()

else:
# Handles normal gene list input
	genes = args.things
	results = geneWordSearch(genes,minChance=args.p)
	resultsPrinter(results,args.w,args.t,out)

out.close()
print('Completed! Check ' + args.o + ' for your results.')




