# SPIMI MERGE
COMP 479 / Fall 2016
Project 1
Jeremy Brown -- ID 27515421


## Application description

### Building the dictionary
#### Fetching the corpus
The script checks if the corpus is present in a predetermined location. If the corpus is not found, it will be
downloaded and extracted prior to continuing. If the --download-corpus flag is specified, the corpus will be
re-downloaded even if it was found.

#### Parsing the corpus
The corpus is parsed using the BeautifulSoup library to find all <REUTERS> tags in each corpus file. Within these tags,
the docID (<NEWID> tag) and the document body (<DOCUMENT><BODY> tag) are parsed to store their containted information.
The document body is then tokenized using nltk's word tokenizer. The term list is then stemmed using the Porter stemmer
if the --stem flag was used when running the script and the stopwords are removed if the --remove-stopwords flag was
used. The list is then turned into a list of (term, docID) pairs.

#### Invert step
The SPIMI inverter is then given the list of (term, docID) pairs, along with parameters such as the maximum block size,
which can be specified with the --limit-block-size command-line flag. It then proceeds to do a read each term in the
list and add it to an inverted index of the form {term: postings_list}. When a new occurrence of a term is found, its
docID is added to the postings list in the inverted index.

Once the maximum block size has been reached, the term block will be sorted and written to a file on disk. Then the
process can start again with the remaining terms until all terms have been stored in block files. The format of the
block file is as follow:

== start of file ==
first_term docID1 docID2 docID3 ...
second_term docID1 docID2 docID3 ...
...
last_term docID1 docID2 docID3 ...
== end of file ==

#### Merge step
The merge step essentially merges all of the separate block files into one master dictionary file. The point of this
instead of putting everything in one file from the start is the memory limitation. Since the master file is too big to
be fully in memory, it is created by reading parts of the individual block files.

The first lines of each block file are read into memory. The terms on these lines are all compared lexicographically to
determine the one that comes first. Once the first term is found, it is written to the master dictionary file along with
its postings list. Then the second line of the block file from which that term came from is read into memory, and the
process continues until all terms from all individual block files have been stored in the master dictionary file. If
a term is present in multiple block files, the postings lists are merged and the resulting list is written to the master
dictionary file.


### Querying the dictionary
Querying is done by first taking the user input and determining the type of query the user would like to run.
This is determined by the first command-line argument being either (AND, and, OR, or).
After that any arguments following the query type are considered to be query keywords.

The keywords are then sorted into a list and the master dictionary file is opened.
Since both the keywords list and the dictionary file are sorted, it is easy to search for each keyword in the dictionary
simply by going through it in order and doing a lexicographical comparison. If a query keyword is found in the
dictionary, its postings list is parsed and stored. This continues until all query keywords have been found or not found
in the dictionary.

Once the postings list for each keyword is determined, the lists are handled depending on the query type. For an AND
query, the postings lists are intersected to keep only the docID's that are common to all the keywords' postings lists.
For an OR query, a union is done to essentially remove the duplicate docID's.

Once the resulting docID's have been determined, they are outputted to the user in the console.


## Sample Runs



## What I have learned

I have learned that the scale at which we often see data is very small relative to the actual range of data available.
Here we are using the Reuters corpus, which contains many thousands of documents, and that is only an infinitely tiny
fraction of what is really available and at scale used by search engines. Considering the inverted index file is only
a few megabytes in size, it is reasonable to understand that a much larger corpus would not easily fit in a computer's
memory.

I also learned that at scale, algorithmic efficiency is very important. Simply having a small part of an algorithm
taking longer than it could if it were optimized, then at a scaled of millions and millions of iterations the
program will take a much longer time to run. This can be easily missed if our sample data is small in size, but by
using larger data sets the difference in time quickly becomes apparent.