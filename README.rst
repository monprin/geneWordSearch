GeneWordSearch
==============

Basic Purpose
-------------

This program takes in names of genes (in one of several ways, see options below), finds the annotations in the in the included databases or a user generate one. It will then sort the annotations it finds based on their frequency in the subset vs their frequency in the database. This is done using a hypergeometric distribution function from scipy. 

Using the command line interface (src/CLI.py) will output the results to a file in one of two formats, a human readable version (default), or a tsv (tab separate value) sheet for further prossesing. It can also take in a single gene and return the network and then do the analysis on that network (maize only).

Use
---

To run this, use the CLI script and run it from the project directory.

It takes in gene identifiers in some form and outputs the words that are associated with those names in order of least likely to occur randomly at the top. It also outputs which genes had which word, and the genes occurrence compared to the total appearances of that word. These are the options, they indicate what type of input and output, make sure to review carefully so your output is everything you hoped it would be.

--buildDB       Indicates the input are database files, will start interactive DB builder. No analysis will be done.
--correctedP    Sorts results by Holm–Bonferroni corrected p values, compensating for the multiple hypothesis problem.
--file          Indicates the input is a file with genes in it.
--folder        Indicates the input are directorys and will process all files in the directory.
--gene_list     Prints list of genes associated with each word.
--help          Show help message (see for shorthand commands).
--low_rep       Prints the words that occur in relatively few of the genes inputed.
--network       Indicates the input are starting points of a network, will first return list of genes in those networks, then traditional output of that list of genes (Only works with maize at the momment).
--out           Location to write the file that contains the results, default is out.txt in current folder.
--prob_cut      This option takes one argument and sets the probability cutoff, default is 0.05.
--species       REQUIRED. Indicates species to use, maize and ath included. More can be added with '--buildDB'.
--tsv           This will give a tsv output for machine readable purposes. Default is human readable output.
--universe      Takes one argument, file with list of genes to use as universe for enrichment query. One gene per line or split by comma.
--webLinks      Outputs associated web links with standard gene output.

This code is hosted on GitHub and can be accessed  `here <https://github.com/monprin/geneWordSearch/>`_. It has a dependency of SciPy. Now on to some examples.

Use and Output Examples
-----------------------

For full output samples, check out `this <https://github.com/monprin/geneWordSearch/tree/master/GeneWordSearch/tests/MaizeIons>`_ folder.

Example 1 (Human Output)
~~~~~~~~~~~~~~~~~~~~~~~~

Input:

::

    $ python3 src/CLI.py --species maize --gene_list --webLinks --file tests/MaizeIons/Al27_candidates.txt

Truncated Output Sample:

::
	
	Multiple Gene Words:
	
	Word: put-169a-panicum
	P-value: 0.000104078977059
	Corrected P-value: 0.233345066566
	Overlap: 370/28229
	Genes Appeared In: grmzm2g000510 grmzm2g001255 grmzm2g001296 ... 
	
	Word: expressed
	P-value: 0.000289040114643
	Corrected P-value: 0.646293696342
	Overlap: 258/19207
	Genes Appeared In: grmzm2g001296 grmzm2g002023 grmzm2g004531 ... 
	
	Word: chromatin
	P-value: 0.00103289214074
	Corrected P-value: 2.30025079743
	Overlap: 14/487
	Genes Appeared In: grmzm2g003002 grmzm2g010342 grmzm2g023983 ...

	...
      
	Web Links associated with these genes:

	ttp://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g164141&modeinput=absolute

	http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g132212&modeinput=absolute
	
	...


Example 2 (Machine Output)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Input:

::

    $ python3 src/CLI.py --species maize --gene_list --webLinks --tsv --file tests/MaizeIons/Al27_candidates.txt

Output Sample:

::

	Word	Pval	CorPval	Ocurrances in Sample	Ocurrances in Database	Genes Appeared In
	Multiple Gene Words:
	put-169a-panicum	0.000104078977059	0.233345066566	370	28229	grmzm2g000510	grmzm2g001255	grmzm2g001296 ...
	expressed	0.000289040114643	0.646293696342	258	19207	grmzm2g001296	grmzm2g002023	grmzm2g004531 ...
	chromatin	0.00103289214074	2.30025079743	14	487	grmzm2g003002	grmzm2g010342	grmzm2g023983 ...
	...
	http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g164141&modeinput=absolute
	http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g132212&modeinput=absolute


How It Works
------------

Finding the Genes
~~~~~~~~~~~~~~~~~

First the command line interface parses the arguments, depending on the task at hand, it will call the geneWordSearch function that does all of the heavy lifting. This function first imports the necessary databases and classes. After that it finds each gene in the database (a pickled python dictionary) and gets their respective lists of annotations. To analyse these annotations, the words are stored as an object with a list of genes being one the attributes. Web links are stored now for later display if desired.

Finding Each Individual Word and Counting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a class for the word that contains all of the statistics within one object, in order to make keeping track of everything easy and clear in the code. The list we created above is now sorted into alphabetical order and instances of each word are created and counted, this avoids computationally costly (on lists) membership tests.

Computing Relative Probability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To do the probability we used the hypergeometric distribution functions in the SciPy library, due to the fact that large factorials are required and are very time consuming, but SciPy can handle this almost instantaneously through what I can only assume is black magic. To compute this, the total word count database is loaded in and searched for the necessary words. What this database is and how it is created is discussed more below. It also computes a corrected probability using the Holm-Bonferroni method to handle the multiple hypothesis test. This value is displayed, but not used to sort or cutoff by default. This can be enabled using the '--correctedP' option.

Printing
~~~~~~~~

Finally the results are printed out using one of two relevant class methods depending on the options set. These are fairly self-explanatory since there are output samples above.

Databases
---------

This code requires three databases that are all included in the package in the databases folder.

Gene Annotations Database
~~~~~~~~~~~~~~~~~~~~~~~~~
This is the database that contains all of the annotations for the specified species genome. It is stored as a pickled dictionary of GeneNote objects corresponding to each gene with its annotations after the words are all split and standardized. There is also a text version of this in a tsv file for reference purposes and error checking.

The program that creates it is DBBuilder.geneWordBuilder. It is run by including the '--buildDB' flag with the main CLI. It also takes in the positional arguments as file paths to the databases you want to use to build. It will ask you a few questions about the file formatting and then process it. It will do this for each file you include and then will save the fresh new database into a folder in the databases folder named after the species name you provided inside the databases folder.

Word Count Database
~~~~~~~~~~~~~~~~~~~

This database is a dictionary that is pickled in the databases folder for the relevant species. There is also a textual representation of this information in a tsv sheet for references purposes.

This is created by the function DBBuilder.totalWordCounts that essentially uses the same algorithm as the main gene word search, but instead of for specific genes, it adds the annotations for all of the genes in the database and just doesn't store some of the superfluous information. It takes no arguments and creates two files in the databases folder. It runs automatically after a new database is created. 

Networks Database
~~~~~~~~~~~~~~~~~

This is a dictionary that contains the lists of genes that are connected. it is a simple mapping from supplied gene to a list of genes. This in the future will be able to be supplied by the end user, but at the moment it is also static. It is created by DBBuilder.networksBuilder which just takes in a tsv and splits the rows. At the moment input needs to be sorted, but that functionality will be added in the future, along with support for arbitrary species, it only works with maize right now.
