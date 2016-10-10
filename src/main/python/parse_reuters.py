#!/usr/bin/python

import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Get all sgm data files in reuters folder
REUTERS_FOLDER = 'reuters21578'
DATA_FILE_SUFFIX = '.sgm'
file_path_prefix = os.path.join(os.getcwd(), REUTERS_FOLDER)

reuters_files = [os.path.join(file_path_prefix, f) for f in os.listdir(REUTERS_FOLDER) if f.endswith(DATA_FILE_SUFFIX)]

# NLTK stopwords
STOPWORDS = set(stopwords.words('english'))

reuters_files = [reuters_files[0]]  # REPLACE ONCE ALGORITHM DONE

tokens_list = list()

for file_path in reuters_files:
    print "Reading {}".format(file_path)

    with open(file_path) as f:
        data = f.read()

    print('Finding documents')

    soup = BeautifulSoup(data, 'html.parser')
    documents = soup.find_all('reuters')

    print("Found {} documents".format(len(documents)))

    #    documents = documents[0:1]  # REPLACE ONCE ALGORITHM DONE

    # Look in all document bodies
    for doc in documents:
        doc_id = int(doc['newid'])
        print("Parsing document {}".format(doc_id))

        if doc.find('body'):
            body_text = str(doc.body.text)

            # tokenize
            term_list = nltk.word_tokenize(body_text)
            # stem & remove stopwords & map
            # stemmer = PorterStemmer()
            # stemmed_tokens = [stemmer.stem(t) for t in tokens if t not in STOPWORDS]
            token_pairs = [(term, doc_id) for term in term_list]
            tokens_list.append(token_pairs)
            # print("Tokenized document {} ({} tokens)".format(doc_id, len(doc_tokens)))

# print("Parsed {} documents and found {} tokens".format(len(documents), len(index)))


from spimi_invert import SpimiInverter

inverter = SpimiInverter(tokens_list)

