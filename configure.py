#!/usr/bin/env python
from __future__ import with_statement
import os
import shutil
import cPickle
import datetime

def main():
    """docstring for main"""

    home = os.getenv("HOME")

    os.chdir(home)

    if os.path.exists(".bashwords/thewords.dat"):
        print("Croiky! You've already got a dictionary.")
        print("I don't want to overwrite your work, so I'll stop.")
        exit()
    else:
        createDict()

    writeToBash()
               
def writeToBash():
    shutil.copy('.bash_profile', '.bash_profile.bak')

    addendum = "# ------for bashwords-------" + \
               "\nalias define='python $HOME/.bashwords/bashwords.py define'" + \
               "\nalias addword='python $HOME/.bashwords/bashwords.py add'" + \
               "\npython ~/.bashwords/cycle.py" + \
               "\nsource ~/.bashwords/exports.sh" + \
               "\n# --------------------------\n\n"

    with open('.bash_profile', 'a') as bash:
        bash.write(addendum)
    
    
def createDict():
    """docstring for createDict"""
    words = []
    sample = {"word": "bucolic",
              "definition": "of or relating to the pleasant aspects" + \
                                " of the countryside or country life",
              "synonyms": ["tranquil", "rustic"],
              "hits": 0,
              "dateInserted": datetime.date.today()}

    words.append(sample)

    with open(".bashwords/thewords.dat", "w") as out:
        cPickle.dump(words, out)
        print("Dictionary created.")

if __name__ == '__main__':
    main()

