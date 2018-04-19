from pathlib import Path
import subprocess

basedir = str(input("Absolute path to the base directory (where\
 all folders to be processed are located):"))

basedir = Path(basedir)
work_file = str(input("Files to be processed:"))
commands = str(input("Commands to be passed:"))

for folder in basedir.iterdir():
    for infile in folder.glob("./*"):
        if infile.is_file() and work_file in str(infile):
            subprocess.Popen(commands.split(),cwd=str(folder)).wait()