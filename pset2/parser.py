__author__="Jose Almaguer <jalmague@gmail.com>"
__date__ ="$Feb 25, 2016"

import sys
import json

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

class CKYParser:
    """
    Class to parse sentences.
    """

    def __init__(self):
        self.unary = {}
        self.binary = {}
        self.nonterm = {}
        self.unary_X = {}

    def train(self, counts_file):
        """
        Function to read in counts file and create dictionary of frequencies.
        """
        for l in counts_file:
            line = l.strip()
            fields = line.split(' ')
            count = int(fields[0])
            rule_type = fields[1]
            key = tuple(fields[2:])
            if rule_type == 'NONTERMINAL':
                self.nonterm[key[0]] = count
            elif rule_type == 'UNARYRULE':
                self.unary[key] = count
                self.unary_X.setdefault(key[0], 0)
                self.unary_X[key[0]] += count
            elif rule_type == 'BINARYRULE':
                self.binary[key] = count
        counts_file.close()

    def binary_rule_probability(self, x, y1, y2):
        """
        Function to calculate the probability that x goes to y1, y2.
        """
        total_count = self.nonterm[x]
        specific_count = self.binary[(x, y1, y2)]
        q = 1.0*specific_count/total_count
        return q

    def unary_rule_probability(self, x, w):
        """
        Function to calculate the probability that x goes to w.
        """
        try:
            total_count = self.unary_X[x]
        except KeyError:
            return 0.0
        try:
            specific_count = self.unary[(x, w)]
        except KeyError:
            return 0.0
        q = 1.0*specific_count/total_count
        return q

    def parse_sentence(self, sentence):
        """
        Method to put together all the pieces and parse a sentence and then output parse tree.
        """
        self.sentence = sentence
        self.initialize_cky_dicts(sentence)
        self.build_cky_dicts(sentence)
        tree = self.construct_tree(sentence)
        return tree

    def initialize_cky_dicts(self, sentence):
        """
        Initializes pi dictionaries in CKY algorithm.
        """
        sentence = ShiftedList(sentence)

        self.pi_dict = {}
        self.bp_dict = {}
        for i in range(1, len(sentence) + 1):
            word = sentence[i]
            word_count = sum(self.unary[key] for key in self.unary if key[1] == word)
            if word_count < 5:
                word = '_RARE_'
            for nonterm in self.nonterm:
                self.pi_dict[(i, i, nonterm)] = self.unary_rule_probability(nonterm, word)

    def build_cky_dicts(self, sentence):
        """
        Builds the pi dictionary and the backpointer dictionary for the
        CKY algorithm.
        """
        for l in range(1, len(sentence)):
            for i in range(1, len(sentence) - l + 1):
                j = i + l
                for nonterm in self.nonterm:
                    rules = set(key for key in self.binary if key[0] == nonterm)
                    max_value = 0.0
                    arg_max = None
                    X, Y, Z = None, None, None
                    for s in range(i, j):
                        for X, Y, Z in rules:
                            try:
                                value = self.binary_rule_probability(X, Y, Z)*self.pi_dict[(i, s, Y)]*self.pi_dict[(s+1, j, Z)]
                            except KeyError:
                                value = 0.0
                            if value > max_value:
                                max_value = value
                                arg_max = ((X, Y, Z), s)
                    self.pi_dict[(i, j, X)] = max_value
                    if arg_max:
                        self.bp_dict[(i, j, X)] = arg_max

    def construct_tree(self, sentence):
        """
        Construct a parse tree using the previously computed CKY backpointer dictionary.
        """
        root = ['SBARQ']
        root = self.add_node(root, 1, len(sentence), sentence)
        return root

    def add_node(self, node, start_position, end_position, sentence):
        """
        Helper method for constructing parse tree from CKY backpointer dictionary.
        """
        if start_position == end_position:
            node.append(sentence[start_position-1])
            return node
        key = (start_position, end_position, node[0])
        value = self.bp_dict[key]
        s = value[1]
        left_root = [value[0][1]]
        right_root = [value[0][2]]
        left_node = self.add_node(left_root, start_position, s, sentence)
        right_node = self.add_node(right_root, s+1, end_position, sentence)
        node.append(left_node)
        node.append(right_node)
        return node

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "incorrect number of arguments"
        sys.exit(1)

    counts_file = sys.argv[1]
    sentence_file = sys.argv[2]
    parse = CKYParser()
    parse.train(open(counts_file, 'r'))

    for l in open(sentence_file, 'r'):
        sentence = l.split()
        tree = parse.parse_sentence(sentence)
        print json.dumps(tree)