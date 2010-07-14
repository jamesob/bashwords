#!/usr/bin/python

from __future__ import with_statement
import random
import cPickle
import os

from setup import installDir
from bashwords import wordbank, word, loadDict

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

    if dict.len == 0:
        os.system('touch %s/exports.sh' % installDir)
        print "Add words to bashwords with `addword'."
        exit()

    word = dict.nextWord()
    del dict # free dict ASAP

    name = word.name
    defin = word.defin
    syns = word.syns

    with open('%s/exports.sh' % installDir, 'w') as f:
        f.writelines(['export currWord="%s"\n' % name,
                      'export currDefinition="%s"\n' % defin,
                      'export currSynonyms="%s"\n' % syns,
                      'PS1="$currWord $PS1"\n'])

if __name__ == '__main__':
    cycle()
