from nltk.stem import PorterStemmer


def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)
