import pickle
import requests
# Save data to a file (will be part of your data fetching script)

def pickler(filename, link):
    """Pickles the data from an html and saves to a variable with the name 'filename'

    """
    link_text = requests.get(link).text
    fout = open(filename, 'wb')
    pickle.dump(link_text, fout)
    fout.close()
    return filename

if __name__ == '__main__':
    pickler('Voyage_To_Jupiter.pickle', 'http://www.gutenberg.org/files/58915/58915-h/58915-h.htm')
