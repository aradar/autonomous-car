#!/usr/bin/env python3

import sys
import os

def print_help():
    print("Help:")
    print("main_unit setup")
    print("main_unit remove")
    print("main_unit install")

def setup_venv():
    os.system("python -m venv ../mu_venv")

def remove_venv():
    os.system("rm -rf ../mu_venv")

def install_reqs():
    os.system("../mu_venv/bin/pip install -r requirements.txt")

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
