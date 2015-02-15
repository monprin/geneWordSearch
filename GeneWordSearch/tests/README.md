Zea Mays Developmental CoExpression Network
===========================================

Given no other information about a gene, a good indicator of its function it its gene expression.
If you measure a genes expression across a slew of different experiments, you can create a gene
*expression profile* which effectively captures, on some level, what a gene is doing (or at least
narrow it down). For example, we measured each genes expression in ~50 different maize tissues
at various time points in development. We can then get an idea of, for any given gene, where it is
being expressed. It could be something like: gene a is expressed in the leaves and roots, but only
during mature development. We then look for other genes which have those same properties. This way we
can group similar groups of genes together based on nothing else but their gene expression profiles.
ZmDevelopmentalNetwork.zip contains these gene-gene interactions. The score column is just a value 
which stores the strength of the interaction (maybe for future filtering). All the interactions in
the file are significant. You can read more about the approach we took and the theory and stuff [here](http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0099193) 

**Given a single gene, give me other genes associated with that gene**

**Given a single gene, give me word enrichment based off its nearest neighbors**



Zea Mays Root MCL Clusters
==========================

[MCL](http://micans.org/mcl/) is a graph clustering algorithm which simulates random walks between nodes to define clusters.
We took gene expression data from 50 different genetically distinct maize lines and created networks based on patterns
of gene expression data. The main idea behind this approach is the following:

+ Maize lines are **very** phenotypically different (think breeds of dogs) but are still the same species
+ Being the same species, they effectively have the same set of genes. Something else must be leading to differences in phenotype
+ The running hypothesis is that changes in gene expression/regulation is responsible for differences in phenotype [Swanson-Wagner et al](http://www.pnas.org/content/109/29/11878.abstract)
+ Genes often act in groups, so genes which are biologically related will have similar patterns of gene expression across experimental conditions.
+ We clustered groups of genes over 50 different maize lines which had similar patterns of genes expression. Since we only know the patterns, we want to find out the biological processes. [More info here](http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0099193)

Each file in this directory is a group a genes defined by MCL. Clusters with lower numbers have more genes (MCL0.txt is the largest, etc.). 

**What do these genes do???**
