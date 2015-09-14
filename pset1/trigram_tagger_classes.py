__author__="Jose Almaguer <jalmague@gmail.com>"
__date__ ="$Sep 13, 2015"

import sys
from collections import defaultdict

def input_file_iterator(input_file):
    """
    Get an iterator object over the input file.  Iterates over each
    word in the file and returns None for blank lines indicating
    sentence boundaries.
    """
    l = input_file.readline()
    while l:
        line = l.strip()
        if line:
            yield line
        else:
            yield None
        l = input_file.readline()

def sentence_iterator(file_iterator):
    """
    Return an iterator object that yields one sentence at a time.
    Sentences are represented as lists of words.
    """
    current_sentence = [] #Buffer for the current sentence
    for l in file_iterator:
        if l == None:
            if current_sentence:  #Reached the end of a sentence
                yield current_sentence
                current_sentence = [] #Reset buffer
            else: # Got empty input stream
                sys.stderr.write("WARNING: Got empty input file/stream.\n")
                raise StopIteration
        else:
            current_sentence.append(l)

    if current_sentence: #If the last line was blank, we're done
        yield current_sentence #Otherwise when there is no more token
                               # in the stream return the last sentence

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

class Sentence:
    """
    Class to create sentences that can be passed to the Viterbi algorithm.
    Uses the correct indexing for the algorithm including returning '*' for
    arguments of -1 and 0 and 'STOP' for the last argument.
    """

    def __init__(self, words):
        self.words = words
        self.length = len(words)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if index in [-1, 0]:
            return '*'
        elif index-1 == self.length:
            return 'STOP'
        elif index in xrange(1, self.length+1):
            return self.words[index-1]
        else:
            raise IndexError('index out of range')

class ShiftedList:
    """
    Class to makes lists with indices starting at 1 rather than 0.
    """
    def __init__(self, original_list):
        self.original_list = original_list
        self.length = len(original_list)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if index in xrange(1, self.length+1):
            return self.original_list[index-1]
        else:
            raise IndexError('index out of range')

    def __setitem__(self, index, value):
        if index in xrange(1, self.length+1):
            self.original_list[index-1] = value
        else:
            raise IndexError('index out of range')

class TrigramTaggerClasses:
    """
    Class to tag words using the Viterbi algorithm on Trigrams.  Uses
    four different classes for rare words.
    """

    def __init__(self):
        pass

    def train(self, counts_file):
        """
        Function to read in counts file and create dictionary of word
        and n-gram counts.
        """
        self.n_gram_dict = {}
        self.counts_dict = defaultdict(int)
        for l in counts_file:
            line = l.strip()
            fields = line.split(' ')
            e_type = fields[1]
            if e_type != 'WORDTAG':
                count = int(fields[0])
                self.n_gram_dict[tuple(fields[2:])] = count
            else:
                count = int(fields[0])
                self.counts_dict[tuple(fields[2:])] = count
        counts_file.close()

    def calculate_ngram(self, trigram):
        """
        Calculate the probability that the third tag in a trigram appears given
        that the first two tags in the trigram appear.
        """
        assert len(trigram) == 3
        trigram_count = self.n_gram_dict[trigram]
        bigram = trigram[:2]
        bigram_count = self.n_gram_dict[bigram]
        q = 1.0*trigram_count/bigram_count
        return q

    def calculate_emission(self, tag, word):
        """
        Calculate emission probability for word and tag combination.  This is
        defined as the probability that a word will appear given the tag.
        """
        tag_word_counts = self.counts_dict[(tag, word)]
        tag_counts = self.n_gram_dict[(tag,)]
        e = 1.0*tag_word_counts/tag_counts
        return e

    def tag_set(self, k):
        """
        Returns the set of possible tags for each position in the sentence.
        """
        if k >= 1:
            return ['O', 'I-GENE']
        else:
            return ['*']

    def build_viterbi_dicts(self, sentence):
        """
        Builds the pi dictionary and the backpointer dictionary for the
        Viterbi algorithm.
        """
        sentence = ShiftedList(sentence)

        self.pi_dict = {}
        self.bp_dict = {}
        self.pi_dict[(0, '*', '*')] = 1.0
        for k in range(1, len(sentence)+1):
            #replace word with appropriate marker if used less than 5 times in training file
            if self.counts_dict[('O', sentence[k])] + self.counts_dict[('I-GENE', sentence[k])] >= 5:
                word = sentence[k]
            else:
                word = classify_word(sentence[k])
            for v in self.tag_set(k):
                for u in self.tag_set(k-1):
                    w_tag_set = self.tag_set(k-2)
                    max_value = 0.0
                    arg_max = w_tag_set[0]
                    for w in w_tag_set:
                        pi = self.pi_dict[(k-1, w, u)]
                        q = self.calculate_ngram((w, u, v))
                        e = self.calculate_emission(v, word)
                        value = pi*q*e
                        #find max_value and arg_max
                        if value > max_value:
                            max_value = value
                            arg_max = w
                    self.pi_dict[(k, u, v)] = max_value
                    self.bp_dict[(k, u, v)] = arg_max

    def extract_tags(self, sentence):
        """
        Extracts tags from previously built Viterbi algorithm dictionaries.
        """
        n = len(sentence)
        y = ShiftedList([None]*n)

        #set y[n-1] and y[n]
        u_tag_set = self.tag_set(n)
        v_tag_set = self.tag_set(n-1)
        max_value = 0.0
        arg_max = (u_tag_set[0], v_tag_set[0])
        for u in u_tag_set:
            for v in v_tag_set:
                value = self.pi_dict[(n, u, v)]*self.calculate_ngram((u, v, 'STOP'))
                #find max_value and arg_max
                if value > max_value:
                    max_value = value
                    arg_max = (u, v)
        y[n-1] = arg_max[0]
        y[n] = arg_max[1]

        for k in range(n-2, 0, -1):
            y[k] = self.bp_dict[k+2, y[k+1], y[k+2]]

        return y.original_list

    def predict_sentence(self, sentence):
        """
        Takes in a sentence and returns a list of tuples of the words of
        the sentence and the predicted tag.
        """
        self.build_viterbi_dicts(sentence)
        tags = self.extract_tags(sentence)
        out_tuples = zip(sentence, tags)
        return out_tuples


    def write_tags(self, input_file, output):
        """
        Writes words with tags to the output file object.
        """
        sentences = sentence_iterator(input_file_iterator(input_file))
        for sentence in sentences:
            tagged_sentence = self.predict_sentence(sentence)
            for word, tag in tagged_sentence:
                output.write(word + ' ' + tag + '\n')
            output.write('\n')

def usage():
    print """
    python trigram_tagger_classes.py [counts_file] [input_file] > [output_file]
    """

if __name__ == '__main__':

    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    counts_file = file(sys.argv[1], 'r')
    input_file = file(sys.argv[2], 'r')

    tagger = TrigramTaggerClasses()
    tagger.train(counts_file)
    tagger.write_tags(input_file, sys.stdout)