# This is the Command Line interface for geneWordSearch.
# Needs to be run from the main program folder.

# Written by Joe Jeffers 

import sys
import math
import pickle
import argparse
from genewordsearch import DBBuilder
from genewordsearch.Classes import WordFreq
from genewordsearch.GeneWordSearch import geneWordSearch

def resultsPrinter(results, web, table, outfile, genes):
# Function to print the results 
	# Input: 
	#	The results from the geneWordSearch function
	#	a boolean for wheather to print links
	#	A boolean for whether it should be table output
	#	A writeable file object
	
	# Split the results
	words = results[0]
	links = results[1]
	
	# Determine the minimum ammount of genes a word must occur in
	# to be printed in the interesting list
	
	if(table):
		# Print the header for the table
		outfile.write(WordFreq.robotHeaders(genes)+ '\n')
	
		# Print the genes by category of multiples and singles
		for item in words:
			outfile.write(item.forRobot(genes) + '\n')
		
		# Prints out web links if needed
		if(web):
			for link in links:
				outfile.write(link + '\n')
	
	else:
		# Print the genes out
		for item in words:
			outfile.write(item.forHuman(genes) + '\n')
	
		# Prints out web links if needed
		if(web):
			outfile.write('Web Links associated with these genes:'+'\n' + '\n')
			for link in links:
				outfile.write(link + '\n' + '\n')

# Setup the Parser
parser = argparse.ArgumentParser(description='Find the important words associated with supplied genes.')
parser.add_argument('-c','--correctedP',dest='c',action='store_true',default=False,help=
'Sorts results by Holm–Bonferroni corrected p values, compensating for the multiple hypothesis problem.')
parser.add_argument('-g','--gene_list',dest='g',action='store_true',default=False,help=
'Prints list of genes associated with each word.')
#parser.add_argument('-l','--low_rep',dest='l',action='store_true',default=False,help=
#'Prints the words that occur in relatively few of the genes inputed.')
parser.add_argument('-o','--out',dest='o',action='store',type=str,default='out.txt',help=
'Location to write the file that contains the results, default is out.txt in current folder.')
parser.add_argument('-p','--prob_cut',dest='p',action='store',type=float,default=0.05,help=
'This option takes one argument and sets the probability cutoff, default is 0.05.')
parser.add_argument('-s','--species',dest='s',action='store',type=str,required=True,help=
'REQUIRED. Indicates species to use, maize and ath included. More can be added with \'--buildDB\'.')
parser.add_argument('-t','--tsv',dest='t',action='store_true',default=False,help=
'This will give a tsv output for machine readable purposes. Default is human readable output.')
parser.add_argument('-u','--universe',dest='u',action='store',type=str,help=
'Takes one argument, file with list of genes to use as universe for enrichment query. One gene per line or split by comma.')
parser.add_argument('-w','--webLinks',dest='w',action='store_true',default=False,help=
'Outputs associated web links with standard gene output.')
parser.add_argument('--buildDB',action='store_true',default=False,help=
'Indicates the input are database files, will start interactive DB builder. No analysis will be done.')
parser.add_argument('--file',action='store_true',default=False,help=
'Indicates the input is a file with genes in it.')
parser.add_argument('--folder',action='store_true',default=False,help=
'Indicates the input are directorys and will process all files in the directory.')
parser.add_argument('--network',action='store_true',default=False,help=
'Indicates the input are starting points of a network, will first return list of genes in those networks, then traditional output of that list of genes (Only works with maize at the momment).')
parser.add_argument('things',action='store',nargs='*')

# Parse the arguments
args = parser.parse_args()
args.s = args.s.lower()

if(args.u):
# Build alternate universe if it is so ordained
	import geneWordSearch.DBBuilder
	genes = []
	geneUni = open(args.u)
	for row in geneUni.readlines():
		rowsy = row[:-1]
		genes += rowsy.split(',')
	DBBuilder.tempBuilder(genes,args.s)
	args.s = 'tmp'
	geneUni.close()
	del genes

if(args.file):
# Deals with input if it is a file name
	genes = []
	for name in args.things:
		geneList = open(name)
		for row in geneList.readlines():
			genes += row.split()
	
	results = geneWordSearch(genes,args.s,minChance=args.p,corrected=args.c)
	
	# Open the output file and write
	out = open(args.o,'w')
	resultsPrinter(results,args.w,args.t,out,args.g)
	out.close()
	print('Completed! Check ' + args.o + ' for your results.')

elif(args.network):
# Deals with finding the gene network and running the relevant analysis
	# Loads the network db and get the genes
	genes = []
	nets = open('databases/'+ args.s +'/networks.p','rb')
	networks = pickle.load(nets)
	nets.close()
	for gene in args.things:
		genes += networks[gene]
	
	# Open the out file and print the network
	out = open(args.o,'w')
	out.write('These are the genes related to the gene(s) you identified:'+'\n')	
	for gene in genes:
		out.write(gene + '\n')
	
	# Run the analysis
	results = geneWordSearch(genes,args.s,minChance=args.p,corrected=args.c)
	
	# Print the Results
	out.write('\n' + 'Results from this list:' + '\n' + '\n')
	resultsPrinter(results,args.w,args.t,out,args.g)
	out.close()
	print('Completed! Check ' + args.o + ' for your results.')

elif(args.folder):
# Deals with directory option by analyzing file by file and doing output
# individually for each file
	# Find the folders indicated by the input
	import glob
	results = []
	for folder in args.things:
		# Find the files in each folder seperately
		if(not(folder[-1] == '/')):
			folder += '/'
		fileList = glob.glob(folder + '*.txt')
		fileList.sort()
		fileList = filter(lambda x: ((len(x) <= 13) or (not(x[-12:] == '_results.txt') and not(x[-16:] == '_results_new.txt'))),fileList)
		
		# For each file, run the analysis and output the results
		for fileName in fileList:
			print('Analysing ' + fileName + '...')
			# Read the genes in the file
			genes = []
			geneList = open(fileName)
			for row in geneList.readlines():
				genes += row.split()
			geneList.close()
			
			# Run the analysis
			results = geneWordSearch(genes,args.s,minChance=args.p,corrected=args.c)
			
			# Print the results
			resultFile = fileName[:-4] + '_results_new.txt'
			out = open(resultFile,'w')
			resultsPrinter(results,args.w,args.t,out,args.g)
			out.close()
		print('Completed folder! Check ' + folder + ' for your results.')

elif(args.buildDB):
# Handles running the database builder program from the main CLI
	DBBuilder.geneWordBuilder(args.s,args.things)
	print('Database has been built in /databases/'+args.s)
	print('Please run this program again to do the gene analysis, and use the options -s to define the species')
	
else:
# Handles normal gene list input
	# Run the analysis
	results = geneWordSearch(args.things,args.s,minChance=args.p,corrected=args.c)
	
	# Print the Results
	out = open(args.o,'w')
	resultsPrinter(results,args.w,args.t,out,args.g)
	out.close()
	print('Completed! Check ' + args.o + ' for your results.')

if(args.u):
# If they used a custom universe, then delete the temp folder and all 
# associated database files
	import shutil
	shutil.rmtree('databases/tmp/')




