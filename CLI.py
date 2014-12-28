
# Command Line interface for geneWordSearch:
from GeneWordSearch import geneWordSearch
import sys
import argparse
from Classes import WordFreq

parser = argparse.ArgumentParser(description='Find the important words associated with supplied genes.')
parser.add_argument('-w',action='store_true',default=False,help='This will output associated weblinks with standard gene output.')
parser.add_argument('-p',action='store',type=float,default=0.05,help='This option takes one argument and sets the probability cutoff, default is 0.2.')
parser.add_argument('-t',action='store_true',default=False,help='This will give a tsv output for machine readable purposes. Default is human readable output.')
parser.add_argument('-f',action='store_true',default=False,help='This indicates that the input strings will be files with genes in them')
parser.add_argument('-d',action='store_true',default=False,help='Indicates that the input is a directory and will process all files in the directory')
parser.add_argument('things',action='store',nargs='*')
args = parser.parse_args()
if(args.f):
	genes = []
	for name in args.things:
		geneList = open(name)
		for row in geneList.readlines():
			genes += row.split()
		results = geneWordSearch(genes,minChance=args.p)


elif(args.d):
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
				print('\n')
				print('Results for ' + fileName + ':')
				print('\n')
				results += geneWordSearch(genes,minChance=args.p)
			geneList.close()

else:
	genes = args.things
	results = geneWordSearch(genes,minChance=args.p)

# Split the results tuple into the relevant pieces
words = results[0]
links = results[1]

# Print the results that are above the chance threshold
# machineRead Parameter prints the output as a tsv sheet to be used for a machine readable format
if(args.t):
	# Print the header for the table
	print(WordFreq.robotHeaders())
	
	# Print the lines using class function
	for item in words:
		print(item.forRobot())
	
	if(args.w):
		for link in links:
			print(link)
	
else:
	
	for item in words:
		print(item.forHuman())
		
	if(args.w):
		print('Web Links associated with these genes:'+'\n')
		for link in links:
			print(link + '\n')
