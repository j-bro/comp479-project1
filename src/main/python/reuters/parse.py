#!/usr/bin/env python2

import os
import sys
import nltk

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # easy hack to import lib module
reload(sys)
sys.setdefaultencoding('utf-8')


class ReutersParser:

    def __init__(self, reuters_folder, stem=False, case_folding=False, no_numbers=False, remove_stopwords=False,
                 data_file_suffix='.sgm', stopwords=set(stopwords.words('english'))):
        """
        Instantiate the object to parse the Reuters corpus.
        :param reuters_folder: the folder where the Reuters corpus is stored.
        :param stem: whether or not to stem the term list (True/False)
        :param case_folding: whether or not to use case folding on the term list (True/False)
        :param no_numbers: whether or not to remove numbers from the term list (True/False)
        :param remove_stopwords: whether or not to remove stopwords from the term list (True/False)
        :param data_file_suffix: the suffix of the Reuters data files.
        :param stopwords: the set of stopwords to use if the remove_stopwords option is selected.
        """
        # Get all sgm data files in reuters folder
        self.reuters_data_folder = reuters_folder
        self.stem = stem
        self.case_folding = case_folding
        self.no_numbers = no_numbers
        self.remove_stopwords = remove_stopwords
        self.data_file_suffix = data_file_suffix
        file_path_prefix = os.path.join(os.getcwd(), reuters_folder)
        self.reuters_files = [os.path.join(file_path_prefix, f) for f in os.listdir(reuters_folder) if f.endswith(data_file_suffix)]
        self.stopwords = stopwords

    def parse(self):
        """
        Parse the Reuters corpus into a list of (term, docID) pairs.
        :return: the list of (term, docID) pairs representing the Reuters corpus.
        """
        tokens_list = list()

        for file_path in self.reuters_files:
            print "Reading {}".format(file_path)
            with open(file_path) as f:
                data = f.read()

            print('Finding documents')
            soup = BeautifulSoup(data, 'html.parser')
            documents = soup.find_all('reuters')
            print("Found {} documents".format(len(documents)))

            print("Parsing documents in {}".format(file_path))
            # Look in all document bodies
            file_token_pairs = list()
            for doc in documents:
                doc_id = int(doc['newid'])

                if doc.find('body'):
                    body_text = str(doc.body.text)

                    # tokenize
                    term_list = nltk.word_tokenize(body_text)

                    # compress if needed
                    term_list = self.compress_terms(term_list)

                    token_pairs = [(term, doc_id) for term in term_list]
                    file_token_pairs.extend(token_pairs)

            print("Found {} tokens in {} documents in file {}.".format(len(file_token_pairs), len(documents), file_path))
            tokens_list.extend(file_token_pairs)

        print("Found {} tokens total.".format(len(tokens_list)))
        return tokens_list

    def compress_terms(self, term_list):
        """
        Stem and remove stopwords
        :param term_list:
        :return:
        """
        # stem & remove stopwords
        if self.remove_stopwords:
            term_list = [t for t in term_list if t not in self.stopwords]
        if self.stem:
            stemmer = PorterStemmer()
            return [stemmer.stem(t) for t in term_list]
        if self.no_numbers:
            term_list = [t for t in term_list if not self.is_number(t)]
        if self.case_folding:
            term_list = [t.lower() for t in term_list]

        return term_list

    @staticmethod
    def is_number(string):
        try:
            int_value = int(string)
        except ValueError:
            return False
        else:
            return True
