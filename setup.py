from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='big-fiubrother-core',
   version='0.7.0',
   description='Big Fiubrother Core Utilities',
   license="GPLv3",
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Eduardo Neira, Gabriel Gayoso',
   author_email='aneira@fi.uba.ar',
   packages=find_packages(),
   install_requires=requirements,
   url='https://github.com/BigFiuBrother/big-fiubrother-core'
)
