#!/usr/bin/env python

from __future__ import with_statement
import os
import shutil
import cPickle

home = os.getenv("HOME")
installDir = home + "/.bashwords/"

def install():
    """docstring for install"""

	# If we haven't created installDir yet...
	if not os.path.exists(installDir):
		print("Creating %s..." % installDir)
		os.mkdir(installDir)

    os.chdir(installDir)

    if os.path.exists("./wordbank.dat"):
        print("Croiky! You've already got a dictionary.")
        overw = raw_input("Wanna overwrite your dictionary? [y/n] ")

        if overw != "y":
            exit()

    writeToBash()
    createDict()

def writeToBash():
    """When we enter this function, we are in installDir."""

    # iffen der bashdefs.sh has already been made, return
    if os.path.exists("bashdefs.sh"):
        print("Skipping .bash_profile modification.")
        return

    # backen up der bash_profile
    shutil.copy(home + '/.bash_profile', home + '/.bash_profile.bak')

    # tell BASHenheim vherein to finden der commands
    defs = "\nalias define='python " + installDir + "/bashwords.py define'" + \
           "\nalias addword='python " + installDir + "/bashwords.py add'" + \
           "\npython " + installDir + "/cycle.py" + \
           "\nsource " + installDir + "/exports.sh\n"

    with open('bashdefs.sh', 'w') as f:
        f.write(defs)

    # source der defs to yon .bash_profile
    bashmod = "# ---------for bashwords-------------\n" + \
              "source "+installDir+"bashdefs.sh\n" + \
              "# -----------------------------------\n"

    with open(home + '/.bash_profile', 'a') as bash:
        bash.write(bashmod)
    
    
def createDict():
    """docstring for createDict"""
    from bashwords import wordbank

    wb = wordbank()
    
    with open("%s/wordbank.dat" % installDir, "w") as out:
        cPickle.dump(wb, out)
        print("Dictionary created.")

if __name__ == '__main__':
    import sys
    arg = sys.argv[1] 

    if arg == "install":
        install()
    else:
        print("Read the docs!")
