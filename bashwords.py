#!/usr/bin/env python

from __future__ import with_statement
import os
import datetime
import cPickle
import random

# where are we?
from setup import installDir

# -------------------
# globals
# -------------------

home  = os.getenv("HOME")
today = datetime.date.today()

# -------------------
# class defs
# -------------------

class word:
    """Holds a single word, its definition, synonyms, hit count, entry date
    and number of days in the bank."""
    
    def __init__(self, word, defin, syns):
        self.name   = word
        self.defin  = defin
        self.syns   = syns
        self.indate = datetime.date.today()
        self.hits   = 0

    def __getState(self):
        """Return all pertinent properties in a dictionary."""
        return [self.name, self.defin, self.syns, self.indate, self.hits]

    def __calcAge(self):
        """Return age of entry in days."""
        return (today - self.indate).days

    age = property(__calcAge, doc="how many days this word has been in bank")
    
    def access(self):
        """Get information, update hit count."""
        self.hits += 1
        return self.__getState()

class wordbank(object):
    """This is our head-honcho; holds all words, average hit count, 
    average age, and manages prioritization."""
    
    def __init__(self):
        """The dictionary "words" holds all words currently in dictionary.
        "wstack" holds words currently cued up."""
        self.words  = []
        self.wstack = []

    def __calcAvg(self, prop):
        """Calculate the average value of some scalar property for each
        word in the dictionary."""

        if len(self.words) == 0:
            return 0
        tot = 0
        for w in self.words:
            tot += getattr(w, prop)
        return tot/len(self.words)

    # lazy evaluation for the win. Properties are for tireless young
    # go-getters who cherish the weekends in sleek, beach-front summerhouses.
    avgAge = property(lambda self: self.__calcAvg("age"), 
                      doc="average age of words")
    avgHits = property(lambda self: self.__calcAvg("hits"), 
                       doc="avg hits on words")

    def __listSorted(self, sortfnc):
        """Print list of word bank entries sorted by some function."""
        self.words.sort(sortfnc)
        for i in self.words:
            print(i.name)

    def __compareBy(self, paramStr): 
        """Return a function that compares two word objects by a specified 
        parameter."""
        return lambda a,b: cmp(getattr(a, paramStr), getattr(b, paramStr))

    def printByAlpha(self): 
        sortfnc = self.__compareBy("name")
        self.__listSorted(sortfnc)

    def add(self):
        """Add a word object to the dictionary."""

        name = raw_input("Title of word: ")
        defin = raw_input("Its definition: ")
        syns = raw_input("Some synonyms? (delimit each with ','): ").split(',') 

        if name not in self.words:
            newword = word(name, defin, syns)
            self.words.append(newword)
        else:
            print("'%s' already in word bank!" % name)

    def remove(self, name):
        """Takes a name (string) of the word to delete then removes it."""

        if name in self.words:
            del self.words[name]
            print("'%s' removed from word bank successfully." % name)
        else:
            print("'%s' not in word bank!" % name)

    def nextWord(self):
        """Pops a random word from the stack and access the word, thereby
        returning the word's information to cycle.py."""

        if self.wstack == []:
            self.__makeStack()
        randword = self.wstack.pop(random.randint(0, len(self.wstack) - 1))
        return randword.access()

    def __makeStack(self):
        """Make a stack of next words 1/5 the size of the word bank.
        Words with lower hit counts are given precedence."""

        # sort words by hits, increasing
        sortByHits = self.__compareBy("hits")
        self.words.sort(sortByHits)
        self.words.reverse()

        # if we've got more than 5 words in the dictionary, make the stack's
        # cardinality one fifth of the word bank's. Otherwise, just add
        # all words to the stack or quit, if we haven't any words.
        if len(self.words) >= 5:
            stackSize = len(self.words)/5
        elif len(self.words) > 0:
            stackSize = len(self.words)
        else:
            print("No words in bank! Quiting.")
            exit()

        for i in range(stackSize):
            self.wstack.append(self.words[i])

# -------------------
# actions
# -------------------

def define(dict):
    """Define the current word according to the env variable."""
    word    = os.getenv("currWord")
    defin   = os.getenv("currDefinition")
    syns    = os.getenv("currSynonyms")

    print("  %s\n  Definition: %s\n  Synonyms: %s"
          % (word, defin, syns))

def add(dict):
    """
    Crack open the dictionary with cPickle, add the word, then
    dump it back to file.
    """

    dict.add()
    
    numEntries = len(dict.words)
    dumpDict(dict)

    print("Word added. %d total words in collection." % numEntries)

def delete(dict):
    """Open the dictionary, delete an entry, dump modified dictionary."""
    mark = raw_input("Word to delete: ").lower()
    dict.remove(mark)
    dumpDict(dict)

def lsWords(dict):
    """List all words currently in dictionary."""
    dict.printByAlpha()

# -------------------
# utilities
# -------------------

def loadDict():
    """Crack the dictionary open, return it."""

    with open("%s/wordbank.dat" % installDir, "r") as f:
        dict = cPickle.load(f)

    return dict

def dumpDict(newDict):
    """Serialize the dictionary back out."""
    
    with open("%s/wordbank.dat" % installDir, "w") as f:
        cPickle.dump(newDict, f)

    return True

if __name__ == '__main__':
    import sys
    choice = sys.argv[1]

    dict = loadDict()

    {'add':     add,
     'define':  define,
     'delete':  delete,
     'lswords': lsWords}[choice](dict)

