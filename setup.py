from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='big-fiubrother-core',
   version='0.0.2',
   description='Big Fiubrother Core Utilities',
   license="GPLv3",
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Eduardo Neira, Gabriel Gayoso',
   author_email='aneira@fi.uba.ar',
   packages=['big_fiubrother_core'],
   url= 'https://github.com/BigFiuBrother/big-fiubrother-core'
)