GeneWordSearch
==============

Basic Purpose
-------------

This program takes in names of genes (in several ways, see options below) and finds the annotations in the database we have associated with those genes in the database. It will sort the annotations it finds based on their frequency in the subset vs their frequency in the database. This is done using a hypergeometric distribution function from scipy. Using the command line interface (src/CLI.py) will output these results to a file in one of two formats, a tsv (tab-separate value) sheet or a more human readable version. It also can take in a single gene and return the network and then do the analysis on that network.

Use
---

To run this, use the CLI script and run it from the project directory.

It takes in gene identifiers in some form and outputs the words that are associated with those names in order of least likely to occur randomly at the top. It also outputs which genes had which word, and the genes occurrence compared to the total appearances of that word. These are the options, they indicate what type of input and output, make sure to review carefully so your output is everything you hoped it would be.

-d	Indicates that the input is a directory and the program will process all files in the directory. (Incompatible with -f and -n)
-f	This indicates that the input strings will be a file with genes in it. (Incompatible with -d and -n)
-n	Indicates that the input is the starting point of a network, will first return list of genes in those networks, then the traditional output on that list of genes. (Incompatible with -d and -f)
-o	Location to write the file that contains the results, default is out.txt in current folder.
-p	This option takes one argument and sets the probability cutoff, default is 0.2.
-t	This will give a tsv output for machine readable purposes. Default is human readable output.
-w	This will output associated web links with standard gene output.

This code is hosted on GitHub and can be accessed  `here <https://github.com/monprin/geneWordSearch/>`_. It also has a dependency of SciPy. Now on to some examples.

Use and Output Examples
-----------------------

Example 1 (Human Output)
~~~~~~~~~~~~~~~~~~~~~~~~

Input:

::

    $ python3 src/CLI.py -w grmzm2g357124 grmzm5g845021

Output Sample:

::

	Word: adenylyl-sulfate
	P-value: 4.17098155238e-10
	Overlap: 3/77
	Genes Appeared In: grmzm5g845021

	Word: ralf
	P-value: 1.08029165324e-07
	Overlap: 2/26
	Genes Appeared In: grmzm2g357124

	Word: virgatum-58684
	P-value: 1.85953766994e-05
	Overlap: 1/1
	Genes Appeared In: grmzm2g357124

    ...
      
    Web Links associated with these genes:
    
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g357124&modeinput=absolute
      
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm5g845021&modeinput=absolute


Example 2 (Machine Output)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Input:

::

    $ python3 src/CLI.py -w -m grmzm2g357124 grmzm5g845021

Output Sample:

::

	Word    Pval    Ocurrances in Sample    Ocurrances in Database  Genes Appeared In
	adenylyl-sulfate        4.17098155238e-10       3       77      grmzm5g845021
	ralf    1.08029165324e-07       2       26      grmzm2g357124
	virgatum-58684  1.85953766994e-05       1       1       grmzm2g357124
    ...
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm2g357124&modeinput=absolute
    http://bbc.botany.utoronto.ca/efp_maize/cgi-bin/efpweb.cgi?primarygene=grmzm5g845021&modeinput=absolute

How It Works
------------

Finding the Genes
~~~~~~~~~~~~~~~~~

First the command line interface parses the arguments, depending on the task at hand, it will call the geneWordSearch function that does all of the heavy lifting. This function first imports the necessary databases and classes. After that it searches through it for each gene and gets a list of the annotations from the database. To analyse these annotations, the words are stored as an object with a list of genes being one the attributes. Web links are stored now for later display if desired.

Finding Each Individual Word and Counting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a class for the word that contains all of the statistics within one object, in order to make keeping track of everything easy and clear int the code. The list we created above is now sorted into alphabetical order and instances of each word are created and counted, this avoids computationally costly membership tests.

Computing Relative Probability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To do the probability we used the hypergeometric distribution functions in the SciPy library, due to the fact that large factorials are required and are very time consuming, but SciPy can handle this almost instantaneously through what I can only assume is black magic. To compute this, the total word count database is loaded in and searched for the necessary words. What this database is and how it is created is discussed more below.

Printing
~~~~~~~~

Finally the results are printed out using one of two relevant class methods depending on the options set. These are fairly self-explanatory since there are output samples above.

Databases
---------

This code requires three databases that are all included in the package in the databases folder.

Gene Annotations Database
~~~~~~~~~~~~~~~~~~~~~~~~~
This is the database that contains all of the annotations for the maize genome that we have. It is stored as pickled list of GeneNote objects that have each gene with its annotations attached after the words are all split as is defined. There is also a text version of this in a tsv file for reference purposes. Eventually one will be able to supply their own database for this but at the moment this is a static database included in the package.

The program that creates it is DBBuilder.geneWordBuilder. It will get generalized to handle more types of files, but for the time being this code is included for reference only.

Word Count Database
~~~~~~~~~~~~~~~~~~~

This database is a dictionary that is pickled in the databases folder. There is also a textual representation of this information in a tsv sheet for references purposes.

This is created by the function DBBuilder.totalWordCounts that essentially uses the same algorithm as the main gene word search, but instead of for specific genes, it adds the annotations for all of the genes in the database and just doesn't store some of the superfluous information. It takes no arguments and creates two files in the databases folder. It takes about 15-30 seconds to run, it should be run whenever the annotation database is edited or added to. Eventually this will be built into a part of a command line interface to use custom databases.

Networks Database
~~~~~~~~~~~~~~~~~

This is a dictionary that contains the lists of genes that are connected. it is a simple mapping from supplied gene to a list of genes. This in the future will be able to be supplied by the end user, but at the moment it is also static. It is created by DBBuilder.networksBuilder which just takes in a tsv and splits the rows. At the moment input needs to be sorted, but that functionality will be added in the future.
