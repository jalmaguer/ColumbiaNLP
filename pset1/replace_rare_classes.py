__author__="Jose Almaguer <jalmague@gmail.com>"
__date__ ="$Sep 13, 2015"

import sys
from collections import defaultdict

"""
Script to replace words with less than 5 appearances in training file.  Rare
words are split up into 4 different classes.  Words with at least one numeric
character are replaced by _NUMERIC_, words that consist entirely of capitalized
letters are replaced by _ALLCAPS_, words that are not all capitals but end with
a capital letter are replaced by _LASTCAP_, and any other rare words is replaced
by _RARE_.
"""

def simple_conll_corpus_iterator(corpus_file):
    """
    Get an iterator object over the corpus file. The elements of the
    iterator contain (word, ne_tag) tuples. Blank lines, indicating
    sentence boundaries return (None, None).
    """
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            # Extract information from line.
            # Each line has the format
            # word pos_tag phrase_tag ne_tag
            fields = line.split(" ")
            ne_tag = fields[-1]
            #phrase_tag = fields[-2] #Unused
            #pos_tag = fields[-3] #Unused
            word = " ".join(fields[:-1])
            yield word, ne_tag
        else: # Empty line
            yield (None, None)
        l = corpus_file.readline()

def create_counts_dict(corpus_iterator):
    """
    Function to create a dictionary of counts for each word in training file.
    """
    counts_dict = defaultdict(int)
    for word, ne_tag in corpus_iterator:
        counts_dict[word] += 1
    return counts_dict

def is_numeric(word):
    """
    Returns true if word contains numeric character.
    """
    return any(char.isdigit() for char in word)

def all_caps(word):
    """
    Returns true if all characters are capital letters
    """
    return all(char.isupper() for char in word)

def last_cap(word):
    """
    Returns true if the last character is a capital letter.
    """
    return word[-1].isupper()

def classify_word(word):
    """
    Function to classify rare words.
    """
    if is_numeric(word):
        return '_NUMERIC_'
    elif all_caps(word):
        return '_ALLCAPS_'
    elif last_cap(word):
        return '_LASTCAP_'
    else:
        return '_RARE_'

def usage():
    print """
    python replace_rare.py [input_file] > [output_file]
    Read in a training file and output training file with rare
    words replaced with tag.
    """

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'one argument expected'
        sys.exit(2)

    #read in file once to count occurences of words
    iterator_file = file(sys.argv[1], 'r')
    corpus_iterator = simple_conll_corpus_iterator(iterator_file)
    counts_dict = create_counts_dict(corpus_iterator)
    iterator_file.close()

    #read in a second time to replace words
    input_file = file(sys.argv[1], 'r')
    output = sys.stdout

    for l in input_file:
        line = l.strip()
        if line:
            fields = line.split(' ')
            ne_tag = fields[-1]
            word = ' '.join(fields[:-1])
            word_count = counts_dict[word]
            if word_count >= 5:
                output.write(word + ' ' + ne_tag + '\n')
            else:
                word_class = classify_word(word)
                output.write(word_class + ' ' + ne_tag + '\n')
        else:
            output.write('\n')
    input_file.close()