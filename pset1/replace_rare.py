import sys
from collections import defaultdict

"""
Script to replace words with less than 5 appearances in training file with _RARE_.
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
                output.write('_RARE_' + ' ' + ne_tag + '\n')
        else:
            output.write('\n')
    input_file.close()