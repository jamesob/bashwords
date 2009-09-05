#!/usr/bin/python
from __future__ import with_statement
import random
import cPickle
import os

# cycle is separated from bashwords.py for the sake of speed;
# since cycle is executed each time a terminal is opened, 
# there's no need for all other functions to be loaded

def cycle():
    """
    Unpickles dictionary, selects a random word, loads relevant
    information into BASH's environment.
    """
    home = os.getenv("HOME")

    with open(home + "/.bashwords/thewords.dat") as f:
        dict = cPickle.load(f)

    currWord = random.sample(dict, 1)[0]

    with open(home + '/.bashwords/exports.sh', 'w') as f:
        f.write('export currWord="%s"\n' % currWord["word"])
        f.write('export currDefinition="%s"\n' % currWord["definition"])
        f.write('export currSynonyms="%s"\n' % currWord["synonyms"])
        f.write('PS1="$currWord|$PS1"\n')                            

if __name__ == '__main__':
    cycle()
