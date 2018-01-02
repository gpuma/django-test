# nlp library
from nltk import tokenize
from nltk.corpus import stopwords
# for command line arguments
import sys

def get_words(filename):
    file = open(filename)
    raw = file.read()
    file.close()
    # tokenizes using english by default
    words = tokenize.word_tokenize(raw)
    filtered_words = [w for w in words if w not in stopwords.words('english')]
    return filtered_words

filename = sys.argv[1]
words = get_words(filename)
print (words)
print("there's %d words" % len(words))