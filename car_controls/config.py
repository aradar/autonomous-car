#!/usr/bin/env python3

import sys
import os

def print_help():
    print("Help:")
    print("config.py setup")
    print("config.py remove")
    print("config.py install")

def setup_venv():
    if sys.platform == "linux":
        os.system("virtualenv2 cc_venv")
    else:
        os.system("virtualenv -p python2.exe ..\\cc_venv")

def remove_venv():
    if  sys.platform != "win32":
        os.system("rm -rf cc_venv")
    else:
        os.system("rmdir /Q /S ..\\cc_venv")

def install_reqs():
    if  sys.platform != "win32":
        os.system("cc_venv/bin/pip install -r requirements.txt")
    else:
        os.system("..\\cc_venv\\Scripts\\pip install -r requirements.txt")

if len(sys.argv) != 2:
    print_help()
    sys.exit()

if sys.argv[1] == "setup":
    setup_venv()

menuoptions = {
    "setup" : setup_venv,
    "remove" : remove_venv,
    "install" : install_reqs
}

if sys.argv[1] in menuoptions.keys():
    menuoptions[sys.argv[1]]()
else:
    print_help()
