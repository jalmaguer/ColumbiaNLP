__author__="Jose Almaguer <jalmague@gmail.com>"
__date__ ="$Feb 21, 2016"

import sys
import json

"""
Script to replace words with less than 5 appearances in training file with _RARE_.
"""

class Replacer:
    """
    Class to count occurences of words in parse tree and then replace rare words
    with a _RARE_ tag.
    """
    
    def __init__(self):
        self.words = {}

    def count(self, tree):
        """
        Count number of occurences of words in tree.
        """
        if isinstance(tree, basestring):
            return

        symbol = tree[0]
        
        if len(tree) == 3:
            y1, y2 = (tree[1][0], tree[2][0])
            self.count(tree[1])
            self.count(tree[2])
        elif len(tree) == 2:
            word = tree[1]
            self.words.setdefault(word, 0)
            self.words[word] += 1
            
    def replace(self, tree):
        """
        After counting use to replace rare words in tree with _RARE_.
        """
        if isinstance(tree, basestring):
            return
        
        symbol = tree[0]
        
        if len(tree) == 3:
            y1, y2 = (tree[1][0], tree[2][0])
            self.replace(tree[1])
            self.replace(tree[2])
        elif len(tree) == 2:
            word = tree[1]
            if self.words[word] < 5:
                tree[1] = '_RARE_'

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'one argument expected'
        sys.exit(2)

    input_file = open(sys.argv[1], 'r')
    output = sys.stdout

    replacer = Replacer()

    trees = []
    for l in input_file:
        tree = json.loads(l)
        trees.append(tree)
        replacer.count(tree)
    input_file.close()

    for tree in trees:
        replacer.replace(tree)
        output.write(json.dumps(tree) + '\n')