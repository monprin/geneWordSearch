# Basic Setup Script
# Requires Python3

# Written by Joseph Jeffers

import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

class SetupDBFolder(install):
    def run(self):
        # Find the database folder
        folder = os.getenv('GWS_STORE', '~/.gws/')

        # Make folders for the default data sets
        zmDir = folder + 'maize'
        atDir = folder + 'ath'
        os.makedirs(zmDir, exist_ok=True)
        os.makedirs(atDir, exist_ok=True)

        # Put the default data in the folders
        shutil.copy('genewordsearch/databases/maize/geneNotes.p', zmDir)
        shutil.copy('genewordsearch/databases/maize/totalWordCounts.p', zmDir)
        shutil.copy('genewordsearch/databases/ath/geneNotes.p', atDir)
        shutil.copy('genewordsearch/databases/ath/totalWordCounts.p', atDir)

        # Run the install process
        install.run(self)

setup(name='GeneWordSearch',
version='2.4.2',
license='GPLv2',
description='Annotation finder for genes.',
author='Joe Jeffers',
author_email='jeffe174@umn.edu',
url='https://github.com/monprin/geneWordSearch/',
packages=find_packages(),
cmdclass={'install': SetupDBFolder},
long_description=open('README.rst').read(),
scripts=['bin/gws'],
install_requires=['flask','numpy','scipy'])
