from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='componentae',
      version=version,
      description="Componentized App Engine",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Izhar Firdaus',
      author_email='kagesenshi.87@gmail.com',
      url='',
      license='MIT',
      packages=['componentae'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'grokcore.component',
        'chameleon',
        'traject'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
