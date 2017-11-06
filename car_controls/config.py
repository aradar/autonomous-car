#!/usr/bin/env python3

import sys
import os

def print_help():
    print("Help:")
    print("config.py setup")
    print("config.py remove")
    print("config.py install")

def setup_venv():
    #os.system("python -m venv venv")
    os.system("virtualenv2 venv")

def remove_venv():
    os.system("rm -rf venv")

def install_reqs():
    os.system("venv/bin/pip install -r requirements.txt")

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
