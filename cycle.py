#!/usr/bin/python

from __future__ import with_statement
import random
import cPickle
import os

from setup import installDir
from bashwords import wordbank, word
# wordbank, word must be included for pickling purposes

# cycle is separated from bashwords.py for the sake of speed;
# since cycle is executed each time a terminal is opened, 
# there's no need for all other functions to be interpreted

def cycle():
    """
    Unpickles dictionary, selects a random word, loads relevant
    information into BASH's environment.
    """
    with open("%s/wordbank.dat" % installDir, "r") as f:
        dict = cPickle.load(f)

    word = dict.nextWord()
    name = word.name
    defin = word.defin
    syns = word.syns

    with open('%s/exports.sh' % installDir, 'w') as f:
        f.write('export currWord="%s"\n' % name)
        f.write('export currDefinition="%s"\n' % defin)
        f.write('export currSynonyms="%s"\n' % syns)
        f.write('PS1="$currWord|$PS1"\n')                            

if __name__ == '__main__':
    cycle()
