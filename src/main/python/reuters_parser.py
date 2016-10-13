import os
import sys
import nltk

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


class ReutersParser:

    def __init__(self, reuters_folder, compress=False, data_file_suffix='.sgm', stopwords=set(stopwords.words('english'))):
        # Get all sgm data files in reuters folder
        self.reuters_data_folder = reuters_folder
        self.compress = compress
        self.data_file_suffix = data_file_suffix
        file_path_prefix = os.path.join(os.getcwd(), reuters_folder)
        self.reuters_files = [os.path.join(file_path_prefix, f) for f in os.listdir(reuters_folder) if
                         f.endswith(data_file_suffix)]
        self.stopwords = stopwords

    def parse(self):
        tokens_list = list()

        self.reuters_files = [self.reuters_files[0]]  # REPLACE ONCE ALGORITHM DONE

        for file_path in self.reuters_files:
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

                    # compression
                    if self.compress:
                        term_list = self.compress_terms(term_list)

                    token_pairs = [(term, doc_id) for term in term_list]
                    tokens_list.extend(token_pairs)
                    # print("Tokenized document {} ({} tokens)".format(doc_id, len(doc_tokens)))

        # print("Parsed {} documents and found {} tokens".format(len(documents), len(index)))
        return tokens_list

    def compress_terms(self, term_list):
        # stem & remove stopwords & map
        stemmer = PorterStemmer()
        return [stemmer.stem(t) for t in term_list if t not in self.stopwords]