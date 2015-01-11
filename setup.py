# Basic Setup Script
# Requires Python3

from setuptools import setup, find_packages

setup(name='GeneWordSearch',
version='0.9',
description='Annotation finder for Maize genes.',
author='Joe Jeffers',
author_email='jeffe174@umn.edu',
packages=find_packages(),
package_data={'databases':['totalWordCounts.*','geneNotes.*','networks.*']},
long_description=open('README').read(),
install_requires=['scipy'])
