# Basic Setup Script
# Requires Python3

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='GeneWordSearch',
version='1.0',
license='GPLv2',
description='Annotation finder for Maize genes.',
author='Joe Jeffers',
author_email='jeffe174@umn.edu',
packages=find_packages(),
package_data={'databases':['totalWordCounts.*','geneNotes.*','networks.*']},
long_description=open('README').read(),
install_requires=['scipy'])
