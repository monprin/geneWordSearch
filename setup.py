# Basic Setup Script
# Requires Python3

# Written by Joseph Jeffers
# Updated Jan 12 2015

# Installs setuptools if needed
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='GeneWordSearch',
version='1.0',
license='GPLv2',
description='Annotation finder for Maize genes.',
author='Joe Jeffers',
author_email='jeffe174@umn.edu',
url='https://github.com/monprin/geneWordSearch/',
packages=find_packages(),
package_data={'databases':['totalWordCounts.*','geneNotes.*','networks.*']},
long_description=open('README.rst').read(),
install_requires=['scipy'])
