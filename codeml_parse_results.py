from Bio.Phylo.PAML import codeml
import os
from itertools import islice
import pandas as pd
import numpy as np
import sys
import argparse

parser = argparse.ArgumentParser(description="Process CODEML model2 orthogroups results into csv file."
                                 " Columns are background w, foreground w and statistically significant BEB sites")
parser.add_argument("[directory]",help="directory with CODEML outputs (make sure they end with .out)")
parser.add_argument("[output name]",help="desired name for csv file")
args = parser.parse_args()

directory = sys.argv[1]

infiles = []
fams_results = {}

for filename in os.listdir(directory):
    if filename.endswith(".out"):
        infiles.append(str(filename))
        
for infile in infiles:
    with open(os.path.join(directory,infile)) as f:
        fore_back_values = []
        beb_values = []
        for line in f:
            if "background w" in line:
                fore_back_values.append(float(line.split()[4]))
            if "foreground w" in line:
                fore_back_values.append(float(line.split()[4]))
            if "Bayes Empirical Bayes (BEB)" in line:
                remaining_lines = "".join(islice(f,None)).split("\n")
                for remaining_line in remaining_lines:
                    if "*" in remaining_line:
                        beb_values.append(int(remaining_line.split()[0]))
        if len(beb_values)<1:
            beb_values = np.nan

        fams_results[infile.split(":")[0]] = [*fore_back_values,beb_values]
        
df = pd.DataFrame.from_dict(fams_results,orient="index")
df = df.fillna(np.nan)
df.columns = ["background_w","foreground_w","BEB_sites"]

df.to_csv("{}.csv".format(sys.argv[2]))