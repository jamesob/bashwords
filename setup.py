#!/usr/bin/env python

from __future__ import with_statement
import os
import shutil
import cPickle

HOME        = os.getenv("HOME") + "/"
INSTALL_DIR = HOME + ".bashwords/"
BASHRC_NAME = ".bashrc"
BASHRC_LOC  = HOME + BASHRC_NAME

def install():
    """Copy some files, source some files, day-in-day-out it's
	the same grind."""

    # If we haven't created INSTALL_DIR yet...
    if not os.path.exists(INSTALL_DIR):
        print("Creating %s..." % INSTALL_DIR)
        os.mkdir(INSTALL_DIR)

	shutil.copy("./setup.py", INSTALL_DIR)
	shutil.copy("./bashwords.py", INSTALL_DIR)
	shutil.copy("./cycle.py", INSTALL_DIR)

    os.chdir(INSTALL_DIR)

    if os.path.exists("./wordbank.dat"):
        print("Croiky! You've already got a dictionary.")
        overw = raw_input("Wanna overwrite your dictionary? [y/n] ")

        if overw != "y":
            exit()

    writeToBash()
    createDict()

def writeToBash():
    """When we enter this function, we are in INSTALL_DIR.
	Ugly string handling, we need to fix that."""

    # iffen der bashdefs.sh has already been made, return
    if os.path.exists("bashdefs.sh"):
        print("Skipping .bash_profile modification.")
        return

    # backen up der bash_profile
    shutil.copy(BASHRC_LOC, BASHRC_LOC + ".bak")

    # tell BASHenheim vherein to finden der commands
    defs = "\nalias defword='python " + INSTALL_DIR + "/bashwords.py define'" + \
           "\nalias addword='python " + INSTALL_DIR + "/bashwords.py add'" + \
           "\nalias lswords='python " + INSTALL_DIR + "/bashwords.py ls'" + \
           "\nalias rmword='python " + INSTALL_DIR + "/bashwords.py delete'" + \
           "\npython " + INSTALL_DIR + "/cycle.py" + \
           "\nsource " + INSTALL_DIR + "/exports.sh\n"

    with open('bashdefs.sh', 'w') as f:
        f.write(defs)

    # source der defs to yon .bash_profile
    bashmod = "# ---------for bashwords-------------\n" + \
              "source "+INSTALL_DIR+"bashdefs.sh\n" + \
              "# -----------------------------------\n"

    if os.system("grep 'for bashwords' %s" % (BASHRC_LOC)) != 0:
        with open(BASHRC_LOC, 'a') as bash:
            bash.write(bashmod)
    
    
def createDict():
    from bashwords import wordbank

    wb = wordbank()
    
    with open("%s/wordbank.dat" % INSTALL_DIR, "w") as out:
        cPickle.dump(wb, out)
        print("Dictionary created.")

if __name__ == '__main__':
    import sys
    arg = sys.argv[1] 

    if arg == "install":
        install()
    else:
        print("Read the docs!")
