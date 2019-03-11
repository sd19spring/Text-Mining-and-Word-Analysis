"""
Mini-Poject 3: Text Mining
AUTHOR: SPARSH BANSAL
"""

import Pickling
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

# I used the Pickling program here which is in a separate text file
# Pickles the html or text file using a book link from the Gutenberg Project Website
# Book 1 - Voyage To Jupiter
Pickling.pickler('Voyage_To_Jupiter.pickle', 'http://www.gutenberg.org/files/58915/58915-0.txt')

# Opens the pickled binary file
open_voyage = open('Voyage_To_Jupiter.pickle', 'rb')
reloaded_copy_of_voyage = pickle.load(open_voyage)

# Writes the pickled file to a text file - getting rid of \r and \n tags
pickled_voyage = open('pickled_voyage.txt', 'w')
for line in reloaded_copy_of_voyage:
    pickled_voyage.write(line)

# Pickling the rest of the books in a similar order
# Book 2 - Dracula
Pickling.pickler('Dracula.pickle', 'http://www.gutenberg.org/ebooks/345.txt.utf-8')
open_dracula = open('Dracula.pickle', 'rb')
reloaded_copy_of_dracula = pickle.load(open_dracula)
pickled_dracula = open('pickled_dracula.txt', 'w')
for line in reloaded_copy_of_dracula:
    pickled_dracula.write(line)

# Book 3 - Alice's Adventures in Wonderland
Pickling.pickler('Alice.pickle', 'http://www.gutenberg.org/ebooks/19033.txt.utf-8')
open_alice = open('Alice.pickle', 'rb')
reloaded_copy_of_alice = pickle.load(open_alice)
pickled_alice = open('pickled_alice.txt', 'w')
for line in reloaded_copy_of_alice:
    pickled_alice.write(line)

# 3 books appended
books = open('books.txt', 'w')
book1 = open('voyage.txt', 'r')
book2 = open('dracula.txt', 'r')
book3 = open('alice.txt', 'r')

for line in book1:
    books.write(line)

for line in book2:
    books.write(line)

for line in book3:
    books.write(line)

# Scrapes the HTML file by removing the HTML tags </p>, </r>, and </n> 
def scraper(input_file):
    """Scrapes the pickled file and makes it usable for the processing functions.

    """
    # Creates an empty list as an empty beginner sentence
    sentence = []
    # Calls the html parser in BeautifulSoup
    html = BeautifulSoup(input_file, 'html.parser')
    # Finds all the tags in the pickled file
    html = html.findAll('p')
    # Substitues all the tags for empty strings
    for line in range(len(html)):
        print(line)
        html = re.sub(r'<.*?>|\r|\n','', str(html[line]))
        sentence.append(html)
    return sentence

# Processes the scraped lines to be (i) all lowercase, (ii) without spaces and line breaks
def get_lines(filename):
    """
    Read all lines from `filename` and return a list of strings,
    one per line, with whitespace stripped from the ends.

    >>> get_lines('My name is Sparsh Bansal. I love doing Reading Journals, but they take a lot of my time.')
    [['my','name','is','sparsh','bansal','i','love','doing','reading','journals','but','they','take','a','lot'
    ,'of','my','time']]
    """
    # Defining the whitespace that will be replaced with punctuation marks in the text processing program
    whitespace_string = ' '
    delete_string = string.punctuation + whitespace_string

    # Defines an empty list as an empty beginner line
    lines = []
    # Opens the file passed in as an argument to the function
    with open(filename) as fp:
        for line in fp:
            processed_line = line.split(' ')
            for word in processed_line:
                test = ''
                # Converts all the non-lowercase words in the lines to lowercase
                processed_word = word.lower()
                for letter in processed_word:
                    if letter not in delete_string:
                        # Deletes the characters in the letters as defined by the string at the start of the function
                        test += letter
                        # Replaces all the line breaks by empty strings
                        final = test.replace("\n",'')
                if final != '':
                    lines.append(final)

    return lines

# First Analysis on the processed text file - Frequency of subject related words
def histogram(l):
    """Return a dictionary that counts occurrences of each word in l.

    """
    # Defines a new dictionary
    d = dict()
    # Assigns all the words to the dictionary and adds one for each words to the frequency histogram
    for w in l:
        d[w] = 1 + d.get(w, 0)

    return d

# __ First Analysis continued __
def most_frequent(l):
    """Returns a list in the descending order of frequency of words in a list of strings.

    """
    # Calls the histogram functioned defined above
    hist = histogram(l)
    # Initializes an empty list 
    list_init = []
    # Appends the frequencies and keys to the list in the format: '(frequency, key)'
    for key, frequency in hist.items():
        list_init.append((frequency, key))
    #Arranges all the list based on the frequency of the keys
    list_init.sort(reverse = True)

    return list_init

# Second Analysis on the processed text file - Markov Analysis on a single book text.
# To prevent skewing of the results due to the book header (Project Gutenberg Header)
def skip_file_header(fp):
    """
    Skips the header of the text file named 'filename' at the point where the Table on
    contents is defined.
    """
    for line in fp:
        if line.startswith('CONTENTS'):
            break

# Initializing the dictionary for mapping the suffixes
suffix_map = {}
# Initializing the global tuple of words
prefix = ()
# Performs Markov Analysis on the given text and generates text
# Used Think Python 'Markov Analysis - Chapter 13' for reference
# User-defined order
def process_file(filename, order=2):
    """
    Traverses the lines and processes every word according to the process_word function
    """
    fp = open(filename)

    # Skips the header information of the book
    #skip_file_header(fp)
    for line in fp:
        # Removes all the trailing characters in the splitted text using rstrip() and splits the text into words using split()
        for word in line.rstrip().split():
            # Calls process_word to process each word
            process_word(word, order)

def process_word(word, order=2):
    """
    Returns a dictionary of suffixes and prefixes
    """
    global prefix
    # Adds the word to the prefix if the string has lesser number of words than the order input (2 in this case)
    if len(prefix) < order:
        prefix += (word,)
        return
            
    try:
        # Appending a word to existing prefix keys - Accounts for multiple words existing for a single prefix key
        suffix_map[prefix].append(word)
    except KeyError:
        # Accounts for the case where a prefix key does not exist for the word being processed
        suffix_map[prefix] = [word]
    # Updates the prefix to move on to the next pair of words
    prefix = shift(prefix, word)

# Changes the processing frame to the next pair of words
def shift(t, word):
    """
    Forms the input tuple for the next frame to be processed -
    1st element of the new tuple (prefix) is the 2nd element from the previous tuple (word)
    2nd element of the new tuple (Word) is the next word in the text file being processed
    """
    return t[1:] + (word,)

# Generates the random text from the processed data - Output of the Markov Analysis
def text_generator(n):
    """
    This fucnction randomly picks words in the original text and generates text based on what these words key to
    in the dictionary.

    My initial plan was to pick words weighted by how frequently they are used in the original text - hence the functions
    most_frequent and histogram

    I pivoted to using unweighted words due to the fact that most commom words turned out to be the common english language 
    words - and, the, a, etc which skewed the text output.
    """
    # Picks the first word for the text
    # It is a randomly selected key from the dictionary of suffixes
    # It is converted to a list as the shift function uses 't' as a list object.
    # random.choice is used because the array of keys is essentially 1-D
    # As an iteration of this program, including the frequency of the keys can be implemented by assigning weights/probabilities
    # to the keys and then randomly selecting the keys
    first_key = random.choice(list(suffix_map.keys()))

    # Creates an empty file to store the Generated Text
    Generated_text = open('Generated.txt', 'w')

    for i in range(n):
        # Indexes to the suffix that maps to the key prefix
        suffixes = suffix_map.get(first_key, None)
        #    Handles the case when the suffix does not map to any prefix in the dictionary
        if suffixes == None:
            # Skips the word and processes the next word
            text_generator(n-i)
            return

        # Chooses a random suffix from the list of suffixes available for a particular key
        word = random.choice(suffixes)
        word_string = str(word) + ' '
        # Writes every word to the .txt file to keep track of text
        Generated_text.write(word_string)
        print(word, end=' ')
        # Re-initializes the key for the next word
        first_key = shift(first_key, word)
    
        

# Third Analysis on the processed text file - Sentiment Analysis on multiple book text.
# Doing Linguistic Post-processing using Vader by the NLTK corpora.
# Calculates the Sentiment scores for all the lines in the file
def analyzer(filename):
    """
    Uses Sentiment Analysis function by NLTK Corpora on the generated text and compares it to the original books
    Cite: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social 
    Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014
    """
    # Opens the file that is input to the function
    fp = open(filename)
    # Calls the Sentiment Intensity Analyzer
    analyzer = SentimentIntensityAnalyzer()
    for line in fp:
        # Calculates the score for each line
        scores = analyzer.polarity_scores(line)
        print(scores)

# Calculates the average scores from the sentiment analyzer
def average_scores(filename):
    """
    Calculates the average scores from the Sentiment Analyzer
    """
    # Initializes the compound score to 0
    compound = 0 
    # Initializes the neg score to 0
    neg = 0 
    # Initializes the neu score to 0
    neu = 0
    # Initializes the pos score to 0
    pos = 0
    # Initializes the number of scores to 0
    number = 0
    # Opens the file that is input to the function
    fp = open(filename)
    analyzer = SentimentIntensityAnalyzer()
    for line in fp:
        score = analyzer.polarity_scores(line)
        compound += score['compound']
        neg += score['neg']
        neu += score['neu']
        pos += score['pos']
        number += 1
    
    # Outputs the average scores for the text file
    string_output = 'For ' + str(filename) + ' the Sentiment scores are as follows:' + '\n' + 'Compound score = ' + str(compound/number) + '\n' + 'Neg score = ' + str(neg/number) + '\n' + 'Neu score = ' + str(neu/number) + '\n' + 'Pos score = ' + str(pos/number)
    return print(string_output)

# Calls the functions in the main screen
if __name__ == '__main__':
    
    # Analysis One - most frequent word analysis in the three books
    print('Analysis I')
    print('\n')
    print('Histogram of words for Voyage to Jupiter')
    print('\n')
    print(most_frequent(get_lines('voyage.txt')))
    print('\n')
    print('Histogram of words for Dracula')
    print('\n')
    print(most_frequent(get_lines('dracula.txt')))
    print('\n')
    print('Histogram of words for Alice in Wonderland')
    print('\n')
    print(most_frequent(get_lines('alice.txt')))
    
    # Analysis Two - Markov Analysis Text Generator 
    print('Analysis II')
    print('\n')
    print('Markov Analysis for Voyage to Jupiter')
    print('\n')
    process_file('voyage.txt', 2)
    print('\n')
    text_generator(200)
    print('\n')
    print('Markov Analysis for Dracula')
    print('\n')
    process_file('dracula.txt', 2)
    print('\n')
    text_generator(200)
    print('\n')
    print('Markov Analysis for Alice in Wonderland')
    print('\n')
    process_file('alice.txt', 2)
    print('\n')
    text_generator(200)
    print('\n')
    print('Markov Analysis for 3 books combined')
    print('\n')
    process_file('books.txt', 2)
    print('\n')
    text_generator(200)
    
    # Analysis Three - Sentiment Analysis 
    #analyzer('voyage.txt')
    #print('\n')
    #analyzer('dracula.txt')
    #print('\n')
    #analyzer('alice.txt')
    #print('\n')
    #analyzer('Generated.txt')
    #print('\n')
    print('Analysis III')
    print('\n')
    print('Sentiment Analysis for Voyage to Jupiter')
    print('\n')
    average_scores('voyage.txt')
    print('\n')
    print('Sentiment Analysis for Dracula')
    print('\n')
    average_scores('dracula.txt')
    print('\n')
    print('Sentiment Analysis for Alice in Wonderland')
    print('\n')
    average_scores('alice.txt')
    print('\n')
    print('Sentiment Analysis for Markov Analysis generated text')
    print('\n')
    average_scores('Generated.txt')