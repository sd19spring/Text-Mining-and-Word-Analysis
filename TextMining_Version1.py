import Pickling
import pickle
import requests
import string
from string import punctuation
from string import whitespace
from bs4 import BeautifulSoup
import re

whitespace_string = ' '
delete_string = string.punctuation + whitespace_string

#Load data from a file (will be part of your data processing script)
#input_file = open('Voyage_To_Jupiter.pickle', 'rb')
#voyage_to_jupiter_full_text = requests.get('http://www.gutenberg.org/files/58915/58915-0.txt').text

Pickling.pickler('Voyage_To_Jupiter.pickle', 'http://www.gutenberg.org/files/58915/58915-h/58915-h.htm')
open_file = open('Voyage_To_Jupiter.pickle', 'rb')
reloaded_copy_of_text = pickle.load(open_file)

#print(reloaded_copy_of_text)

#html = BeautifulSoup(reloaded_copy_of_text, 'html.parser')
#text = html.findAll('p')
#html.find('p')  # find the first paragraph
#str(html.find('p'))  # the first paragraph, as a string. Includes embedded <b> etc.
#for i in range(len(text)):
#    a = re.sub(str('<p>'), '', text[i])
#    print(a)
#text_1 = re.sub(r'<.+?>', '', text)
#one = re.sub(r'/r', '', text_1)

#print(one)
#for link in soup.find_all('a'):
#    print(link.get('href')

def scraper(input_file):
    """Scrapes the pickled file and makes it usable for the processing functions.
    """
    sentence = []
    html = BeautifulSoup(input_file, 'html.parser')
    html = html.findAll('p')
    for line in range(len(html)):
        print(line)
        html = re.sub(r'<.*?>|\r|\n','', str(html[line]))
        sentence.append(html)
    return sentence

def get_lines(filename):
    """
    Read all lines from `filename` and return a list of strings,
    one per line, with whitespace stripped from the ends.

    >>> get_lines('My name is Sparsh Bansal. I love doing Reading Journals, but they take a lot of my time.')
    [['my','name','is','sparsh','bansal','i','love','doing','reading','journals','but','they','take','a','lot'
    ,'of','my','time']]
    """

    lines = []

    with open(filename) as fp:
        for line in fp:
            processed_line = line.split(' ')
            for word in processed_line:
                test = ''
                processed_word = word.lower()
                for letter in processed_word:
                    if letter not in delete_string:
                        test += letter
                        final = test.replace("\n",'')
                if final != '':
                    lines.append(final)

    return lines

def histogram(l):
    """Return a dictionary that counts occurrences of each word in l.

    """
    d = dict()

    for w in l:
        d[w] = 1 + d.get(w, 0)

    return d

def most_frequent(l):
    """Returns a list in the descending order of frequency of words in a list of strings.

    """
    hist = histogram(l)

    list_init = []

    for key, frequency in hist.items():
        list_init.append((frequency, key))

    list_init.sort(reverse = True)

    return list_init


if __name__ == '__main__':
    #print(most_frequent(get_lines('Voyage_To_Jupiter_Downloaded.txt')))
    print(scraper(open_file))