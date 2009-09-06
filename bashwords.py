#!/usr/bin/env python
from __future__ import with_statement
import optparse
import os
import datetime
import cPickle
import random

# -------------------
# globals
# -------------------

home = os.getenv("HOME")

# -------------------
# actions
# -------------------

def define():
    """Define the current word according to the env variable."""
    word    = os.getenv("currWord")
    defin   = os.getenv("currDefinition")
    syns    = os.getenv("currSynonyms")

    print("  %s\n  Definition: %s\n  Synonyms: %s"
          % (word, defin, syns))

def add():
    """
    Crack open the dictionary with cPickle, add the word, then
    dump it back to file.
    """
    dict = loadDict()

    word = raw_input("Which word would you like to add?: ").lower()
    defin = raw_input("Its definition?: ")
    syns = raw_input("Some synonyms? (delimit each with ','): ").split(',') 

    newEntry = {"word": word,
                "definition": defin,
                "synonyms": syns,
                "hits": 0,
                "dateInserted": datetime.date.today()}

    dict.append(newEntry)
    numEntries = len(dict)

    dumpDict(dict)

    print("Word added. %d total words in collection." % numEntries)

def delete():
    """Open the dictionary, delete an entry, dump modified dictionary."""
    dict = loadDict()

    mark = raw_input("Word to delete: ").lower()

    index = -1

    for i in dict:
        if i["word"] == mark:
            index = dict.index(i)
    
    if index == -1:
        print("'%s' not found. No modifications made." % mark)
    else:
        del dict[index]
        print("Entry for '%s' successfully removed." % mark)

    dumpDict(dict)

def lsWords():
    """List all words currently in dictionary."""

    dict = loadDict()
    dict = alphaSort(dict)
    for i in dict:
        print(i['word'])

# -------------------
# utilities
# -------------------

def loadDict():
    """Crack the dictionary open, return it."""

    with open(home + "/.bashwords/thewords.dat", "r") as f:
        dict = cPickle.load(f)

    return dict

def dumpDict(newDict):
    """Serialize the dictionary back out."""
    
    with open(home + "/.bashwords/thewords.dat", "w") as f:
        cPickle.dump(newDict, f)

    return True

def alphaSort(dict):
    """Sorts a list of dictionaries alphabetically
    alphacmp = lambda a,b: cmp(a['word'], b['word'])

    dict.sort(alphacmp)

    return dict
    
if __name__ == '__main__':
    import sys
    choice = sys.argv[1]

    {'add':     add,
     'define':  define,
	 'delete':  delete,
     'lswords': lsWords}[choice]()

