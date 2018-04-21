'''Iterate multiple folders running command line arguments or other
scripts'''

from pathlib import Path
import subprocess
import argparse

#############################ARGPARSER##########################################

parser = argparse.ArgumentParser(description="Iterate multiple folders running \
command line arguments or other scripts",
epilog="Don't add flags to enter values from within script")

parser.add_argument("-bd","--basedir",
action="store",help="absolute path to directory where all folders to be \
processed are located)")
parser.add_argument("-c","--commands",
action="store",help="commands to be passed, as you would from the \
command line")
parser.add_argument("-f","--files",
action="store",default=".",help="Files to be processed (name or extension)")

args = parser.parse_args()

################################################################################

if args.basedir and args.commands and args.files:
    basedir = args.basedir
    commands = args.commands
    work_file = args.files
else:
    basedir = str(input("Absolute path to the base directory (where \
    all folders to be processed are located):"))

    work_file = str(input("Files to be processed:"))
    commands = str(input("Commands to be passed (as you would from the command \
    line):"))

basedir = Path(basedir)

for folder in basedir.iterdir():
    for infile in folder.glob("./*"):
        if infile.is_file() and work_file in str(infile):
            subprocess.Popen(commands.split(),cwd=str(folder)).wait()


#TODO: add option to work on only one folder and allow multiple commands
