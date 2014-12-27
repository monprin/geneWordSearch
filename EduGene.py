# v0.3 Gene Word Cloud Program
# Joe Jeffers

# Command Line interface:
from GeneWordSearch import geneWordSearch
import sys
import argparse
parser = argparse.ArgumentParser(description='Find the important words associated with supplied genes.')
parser.add_argument('-w',action='store_true',default=False,help='This will output associated weblinks with standard gene output.')
parser.add_argument('-p',action='store',type=float,default=0.05,help='This option takes one argument and sets the probability cutoff, default is 0.2.')
parser.add_argument('-m',action='store_true',default=False,help='This will give a tsv output for machine readable purposes. Default is human readable.')
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
		geneWordSearch(genes,webLinks=args.w,minChance=args.p,machineRead=args.m)


elif(args.d):
	import glob
	
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
				geneWordSearch(genes,webLinks=args.w,minChance=args.p,machineRead=args.m)
			geneList.close()

else:
	genes = args.things
	geneWordSearch(genes,webLinks=args.w,minChance=args.p,machineRead=args.m)
