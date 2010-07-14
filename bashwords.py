#!/usr/bin/env python

from __future__ import with_statement
import os
import sys
import datetime
import cPickle
import random

# where are we?
from setup import INSTALL_DIR

# -------------------
# globals
# -------------------

home  = os.getenv("HOME")
today = datetime.date.today()

DEBUG = 1

def dprint(str):
    """For debugging."""
    if DEBUG:
        print str

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

    def __repr__(self):
        return "word '%s'" % self.name

class wordbank(object):
    """This is our head-honcho; holds all words, average hit count, 
    average age, and manages prioritization."""

    def bankTransaction(func):
        """
        A decorator which ensures functions serialize a modified `wordbank` out.
        """
        def trans(*args):
            self = args[0]
            ret = func(*args)
            self._dump()
            return ret
        return trans
    
    def __init__(self):
        """
        `words` holds all words in `wordbank`.
        `cache` holds a certain number of words ready to be accessed.
        """
        self.words = []
        self.cache = []

    def _calcAvg(self, prop):
        """Calculate the average value of some scalar property for each
        word in the dictionary."""

        if len(self.words) == 0:
            return 0
        tot = 0
        for w in self.words:
            tot += getattr(w, prop)
        return tot/len(self.words)

    def _compareBy(self, paramStr): 
        """Return a function that compares two word objects by a specified 
        parameter."""
        return lambda a,b: cmp(getattr(a, paramStr), getattr(b, paramStr))
     
    avgAge = property(lambda self: self._calcAvg("age"), 
                      doc="average age of words")
    avgHits = property(lambda self: self._calcAvg("hits"), 
                       doc="avg hits on words")
    len     = property(lambda self: len(self.words))

    def _dump(self):
        """Serialize the dictionary back out."""
        with open("%s/wordbank.dat" % INSTALL_DIR, "w") as f:
            cPickle.dump(self, f)

    def sort(self, sortfnc):
        self.words.sort(sortfnc)

    def listSorted(self, sortfnc=None):
        """
        Print list of word bank entries sorted by some function.

        TODO: size columns based on max length of words.
        """
        sortfnc = sortfnc or self._compareBy("name")
        self.sort(sortfnc)
        if sys.version_info >= (2, 6):
            print "{0:<25s} {1:<6s} {2:<6s}".format("name", "hits", "age (days)")
            print
            for w in self.words:
                print "{0:<25s} {1:<6d} {2:<6d}".format(w.name, w.hits, w.age)
        else:
            print "%25s %6s %6s" % ("name", "hits", "age (days)")
            print
            for w in self.words:
                print "%25s %6d %6d" % (w.name, w.hits, w.age) 
    def printByAlpha(self): 
        sortfnc = self._compareBy("name")
        self._listSorted(sortfnc)

    @bankTransaction
    def add(self):
        """Add a word object to the dictionary."""

        name = raw_input("Title of word: ")
        defin = raw_input("Its definition: ")
        syns = raw_input("Some synonyms? (delimit each with ', '): ").split(', ') 

        if name not in self.words:
            newword = word(name, defin, syns)
            self.words.append(newword)
        else:
            print("'%s' already in word bank!" % name)
    
    @bankTransaction
    def remove(self, name):
        """Takes a name (string) of the word to delete then removes it."""
        if name in self.words:
            del self.words[name]
            print("'%s' removed from word bank successfully." % name)
        else:
            print("'%s' not in word bank!" % name)

    @bankTransaction
    def nextWord(self):
        """Pops a random word from the stack and access the word, thereby
        returning the word's information to cycle.py."""
        dprint(self.cache)
        if not self.cache:
            self._populateCache()

        word = self.cache.pop(0)
        word.access()
        return word

    def _populateCache(self):
        """Build a cache for `nextWord`."""
        cacheSize = self.len/3 + 1
        self.sort(self._compareBy("hits"))
        for i in range(cacheSize):
            self.cache.append(self.words[i])
    
    def toFile(self, filename):
        """Outputs all words in wordbank to file."""
        with open(filename, "w") as f:
            for w in self.words:
                synstring = ""
                for syn in w.syns:
                    synstring += syn + ","
                synstring = synstring[:-1]
                wordinfo = [w.name, w.defin, synstring, ""]
                wordinfo = [l + "\n" for l in wordinfo]
                f.writelines(wordinfo)

    @bankTransaction
    def fromFile(self, filename):
        """Intakes words from a file."""
        with open(filename, "r") as f:
            lines = f.readlines()
            lines = [l.rstrip('\n') for l in lines]
            while lines != []:
                name = lines.pop(0)
                defin = lines.pop(0)
                syns = lines.pop(0).split(',')
                newword = word(name, defin, syns)
                self._shortAdd(newword)
                # remove hits, newline
                lines.pop(0)
        self._dump()

    @bankTransaction
    def _shortAdd(self, word):
        if word.name not in self.words:
            self.words.append(word)
            self._dump()
        else:
            print("'%s' already in word bank!" % name)
     
# -------------------
# actions
# -------------------

def define(dict):
    """Define the current word according to the env variable."""
    word  = os.getenv("currWord")
    defin = os.getenv("currDefinition")
    syns  = os.getenv("currSynonyms")

    print("  %s\n  Definition: %s\n  Synonyms: %s"
          % (word, defin, syns))

def add(dict):
    """
    Crack open the dictionary with cPickle, add the word, then
    dump it back to file.
    """
    dict.add()
    print("Word added. %d total words in collection." % dict.len)

def delete(dict):
    """Open the dictionary, delete an entry, dump modified dictionary."""
    mark = raw_input("Word to delete: ").lower()
    dict.remove(mark)

def lsWords(dict):
    """List all words currently in dictionary."""
    dict.listSorted()

def toFile(dict):
    filename = raw_input("Name of file to write to: ")
    dict.toFile(filename)

def fromFile(dict):
    filename = raw_input("Name of file to extract from: ")
    dict.fromFile(filename)

# -------------------
# utilities
# -------------------

def loadDict():
    """Crack the dictionary open, return it."""
    with open("%s/wordbank.dat" % INSTALL_DIR, "r") as f:
        dict = cPickle.load(f)
    return dict

if __name__ == '__main__':
    import sys
    choice = sys.argv[1]
    dict   = loadDict()

    {'add':      add,
     'define':   define,
     'delete':   delete,
     'ls':       lsWords,
     'toFile':   toFile,
     'fromFile': fromFile}[choice](dict)

