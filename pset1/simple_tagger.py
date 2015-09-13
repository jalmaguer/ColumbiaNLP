__author__="Jose Almaguer <jalmague@gmail.com>"
__date__ ="$Sep 11, 2015"

import sys
from collections import defaultdict

"""
Simple tagger that tags words based on having the highest
emission probability.
"""

def create_dict(counts_file):
    """
    Create dictionary of word frequencies and (word, token) frequencies.
    """
    counts_dict = defaultdict(int)
    for l in counts_file:
        line = l.strip()
        fields = line.split(' ')
        e_type = fields[1]
        if e_type == 'WORDTAG':
            assert len(fields) == 4
            count = int(fields[0])
            ne_tag = fields[2]
            word = fields[3]
            counts_dict[(word, ne_tag)] = count
            counts_dict[ne_tag] += count
    return counts_dict

def count_occurences(word, counts_dict):
    """
    Count the number of times a word appears as each tag and return as tuple.
    """
    o_counts = counts_dict[(word, 'O')]
    gene_counts = counts_dict[(word, 'I-GENE')]
    return o_counts, gene_counts

def calculate_emission(word, ne_tag, counts_dict):
    """
    Calculate emission probability for word and tag combination.  This is
    defined as the probability that a word will appear given the tag.
    """
    word_count = counts_dict[(word, ne_tag)]
    ne_tag_count = counts_dict[ne_tag]
    emission = float(word_count)/float(ne_tag_count)
    return emission

def usage():
    print """
    python simple_tagger.py [counts_file] [input_file] > [output_file]
    Read in a word count file and a file to be tagged and out a new file
    with the words tagged
    """

if __name__ == '__main__':

    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    counts_file = file(sys.argv[1], 'r')
    counts_dict = create_dict(counts_file)
    counts_file.close()

    dev_file = file(sys.argv[2], 'r')
    out_file = sys.stdout

    for l in dev_file:
        line = l.strip()
        if line:
            rare = sum(count_occurences(line, counts_dict)) < 5
            if rare:
                prediction = max(['O', 'I-GENE'], key=lambda x: calculate_emission('_RARE_', x, counts_dict))
                out_file.write(line + ' ' + prediction + '\n')
            else:
                prediction = max(['O', 'I-GENE'], key=lambda x: calculate_emission(line, x, counts_dict))
                out_file.write(line + ' ' + prediction + '\n')
        else:
            out_file.write('\n')

    dev_file.close()