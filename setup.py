# Basic Setup Script
# Requires Python3

from setuptools import setup, find_packages

setup(name='GeneWordSearch',
version='0.9',
description='Annotation finder for Maize genes.',
author='Joe Jeffers',
author_email='jeffe174@umn.edu',
packages=['Classes','GeneWordSearch']
package_data={'databases/totalWordCounts.p':['databases/totalWordCounts.p'],'databases/geneNotes.p':['databases/geneNotes.p']},
long_description=open('README.md').read(),
install_requires=['scipy'])
