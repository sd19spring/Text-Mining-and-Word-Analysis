.. TextMining-sbansal22

:Name: Text Mining Project
:Author: Sparsh Bansal
:Version: 3.0

Text Mining is a project in Software Design at Olin College of Engineering. It
conducts the following analyses on a given text:

:i: Pickles the books from a given web link 

:ii: Analysis 1 - Word Frequency Analysis

:iii: Analysis 2 - Markov Analysis

:iv: Analysis 3 - Sentiment Analysis

Requirements
============

Text Mining Version 3.0 requires the following Python packages

.. code-block:: python

    import pickle
    import requests
    import string
    from string import punctuation
    from string import whitespace
    from bs4 import BeautifulSoup
    import re
    import sys
    import random
    import numpy as np
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

Installation
============

The easiest and fastest way to get the packages up and running:

.. code-block:: python

    import requests
    print(requests.get('http://google.com').text)

.. code-block:: python
    $ python -m nltk.downloader all
  
Documentation
=============

I have added comments for every line of code that I felt could be beneficial for someone to understand the program

Note: I haved added comments especially on the imported packages and code so that I can fully understand the code written 
by someone else. I have cited the sources wherever appropriate. 

Contributing
============

I used information from:

:i: Think Python - Allen Downey

:i: Vader - NLTK Corpora

Citing
======

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social 
Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014

https://www.greenteapress.com/thinkpython/thinkpython.pdf
