geneWordSearch
==============

##What it Does##

It takes in gene "names" and outputs the words that are associated with those names in order of least likely to occur randomly at the top. It also outputs which genes had which word, and the genes occurance compared to the total apearances of that word. There are three options:

* -w This will print the web links associated with the genes at the bottom of the output
* -p This changes the probability cutoff for printing the gene, the default is 1/20% odds this word occured by chance.
* -m This changes the output to a "machine readable" format, this is just a tab-separated table. The first example is the default human readable format, the second is the machine version.

This code is hosted on GitHub and can be accessed [here](https://github.com/monprin/geneWordSearch/). It also has a dependency of SciPy. Now on to some examples.

##Examples##

###Example 1###

Input:
`$ python3 EduGene.py -w grmzm2g357124 grmzm5g845021`

Output([Full Output](http://www.monprin.com/CompBio/12022014/Human.txt)):
    
    Word: virgatum-58684
    P-value: 0.0
    Overlap: 1/1
    Genes Appeared In: grmzm2g357124
     
    Word: loc100284520
    P-value: 0.0
    Overlap: 1/1
    Genes Appeared In: grmzm2g357124
    
    Word: adenylyl-sulfate
    P-value: 1.26931033738e-13
    Overlap: 3/77
    Genes Appeared In: grmzm5g845021
    
    ...
      
    Web Links associated with these genes:
    
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g357124&modeinput=absolute
      
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm5g845021&modeinput=absolute

###Example 2###

Input:

`$ python3 EduGene.py -w -m grmzm2g357124 grmzm5g845021`

Output([Full Output](http://www.monprin.com/CompBio/12022014/Robot.txt))

    Word	Pval	Ocurrances in Sample	Ocurrances in Database	Genes Appeared In
    virgatum-58684	0.0	1	1	grmzm2g357124
    loc100284520	0.0	1	1	grmzm2g357124
    adenylyl-sulfate	1.26931033738e-13	3	77	grmzm5g845021
    ...
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g357124&modeinput=absolute
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm5g845021&modeinput=absolute

##How It Works##

###Finding the Genes###

First there is a little blurb at the bottom that handles the command line arguments and calls the 'geneWordSearch' function that doess all of the heavy lifting. This function first goes about building the gene annotation database (see details below) using a function. After that it searches through it for each gene and gets a list of the annotations from the database. To analyse these annotations, the words are split up using the regular expressions split funtion and stored as a list of words. Web links are also removed and stored now for later printing.

###Finiding Each Individual Word and Counting###

There is a class for the word that contains all of the statistics within one object, in order to make keeping track of everything easy and clear int the code. The list we created above is now sorted into alphabetical order and instances of each word are created and counted, this avoids computationally costly membership tests.

###Computing Relative Probability###

To do the probability we used the hypergeometric distribution funtions in the SciPy library, due to the fact that large factorials are required and are very time consuming, but SciPy can handle this almost instantaniously through what I can only assume is black magic. To compute this, the total word count database is loaded in and searched for the necessary words. What this database is and how it is created is disscussed more below.

###Printing###

Finally the results are printed out using one of two 'toString' class methods depending on the options set. These are fairly self-explanatory since there are output samples above.

##Databases##

This code requires two databases to function, the first of these is the table of all the genes with their annotations and a few other bits of information that are mostly unused at the momment (See first section for more info). The other is the table contating all of the words in the database, along with how many times it appears in the whole database (See second section). Finally, there is a function that creates the word count database (See second section).

###Gene Annotations Databse###

What follows is a sampling of the database with the headers of the respective columns, it is approximately 65,000 lines long. Sometimes there are annotations, sometimes there are not. This table was also edited from the original so all letters are lowercase to help with matching. The elipses represent that there is more, but for purposes of space, it was removed.

<table>
		<tr>
			<td>maize locus identifier</td>
			<td>...</td>
			<td>maizesequence.org functional description</td>
			<td>bfgr maize functional description</td>
			<td>pfam domain	rice best hit</td>
			<td>...</td>
		</tr>
		<tr>
			<td>grmzm2g410963</td>
			<td>...</td>
			<td>phytosulfokine receptor precursor, putative</td>
			<td>sb04g003870.1</td>
			<td>leucine-rich repeat receptor-like kinase</td>
			<td>...</td>
		</tr>
		<tr>
			<td>grmzm2g063733</td>
			<td>...</td>
			<td> </td>
			<td> </td>
			<td> </td>
			<td>...</td>
		</tr>
		<tr>
			<td>grmzm2g403475</td>
			<td>...</td>
			<td>glycosyl hydrolase, putative, expressed</td>
			<td>sb08g020700.1</td>
			<td>chitinase 1</td>
			<td>...</td>
		</tr>
	</table>

Full version can be found in the databases folder of the repository.

###Word Count Database###

This database is a n-by-2 table that lists each potential word in the annotation database. It looks a bit like this:

<table>
	<tr>
		<td>Frequency</td>
		<td>Word</td>
	</tr>
	<tr>
		<td>121359</td>
		<td>protein</td>
	</tr>
	<tr>
		<td>70017</td>
		<td>1</td>
	</tr>
	<tr>
		<td>63540</td>
		<td>Web Links</td>
	</tr>
	<tr>
		<td>52644</td>
		<td>unknown</td>
	</tr>
	<tr>
		<td>...</td>
		<td>...</td>
	</tr>
</table>

Full version is in the databases folder in the repository.

This is created by a function that essentially uses the same algorithm as the main gene word search, but instead of for specific genes, it adds the annotations for all of the genes in the database and just stores this as a stripped down version of the main class. The class was actually originally for this program. It takes no arguments and replaces the 'totalWordCount.txt' in the program folder. It takes about 15-30 seconds to run, it should be run whenever the annotation database is edited.
