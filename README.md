
# bashwords - a work in progress
by jamesob

* bashwords is a very minimal vocabulary trainer for the BASH
  environment. It was designed with simplicity at the forefront.

  Basically, all it does is affixes a pseudo-random vocabulary
  word from a user-defined (that's you) dictionary to your
  command prompt; e.g,

    analgesic|host:dir usr$
    apropos|host:dir usr$
    bucolic|host:dir usr$

## Unsure of a word's meaning? Use "define".

    analgesic|host:dir usr$ define
    analgesic
    Definition: acting to relieve pain
    Synonyms: ['anesthetic', ' anodyne']
  
## Like to add a word? Use "addword".

    analgesic|host:dir usr$ addword
    Which word would you like to add?: ameliorate
    Its definition?: make something (bad or unsatisfactory) better
    Some synonyms? (delimit each with ','): enhance, alleviate 
    Word added. 4 total words in collection.

## How about deleting? Use "delword".

    analgesic|host:dir usr$ delword
    Word to delete: ameliorate
    Entry for 'ameliorate' successfully removed.

## List all words in dictionary with "lswords".

## Batch import words with "python bashwords.py fromFile".
  File format:
      [name of word]
      [definition]
      [synonyms]
      [blank line]

  Dump all words currently in bank to file with
  "python bashwords.py toFile". File comes in same format as above.

  ------------------------

  Bashwords has, by no means, been optimized for performance and I
  won't be held liable if you ralph while browsing the source.

* to install
    (0. crack open setup.py and specify an install directory
        if you want somewhere other than the default, 
        "~/.bashwords/")
    1. run "python setup.py install"

    
Copyright (c) 2009 James O'Beirne

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
