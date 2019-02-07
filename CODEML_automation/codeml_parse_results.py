import os
from itertools import islice
import pandas as pd
import numpy as np
import sys
import argparse

################################################################################

parser = argparse.ArgumentParser(description="Process CODEML model2 orthogroups results into csv file."
                                 " Columns are background w, foreground w and statistically significant BEB sites")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--m0", help="process model0")
group.add_argument("--m2", help="process model2")
group.add_argument("--both", help="process model0 and model2")

parser.add_argument("directory or directories",nargs="*",default=os.getcwd(),
                    help="directory with CODEML outputs (make sure they end with .out)")

parser.add_argument("[output name]", help="desired name for csv file")
args = parser.parse_args()
################################################################################

def infile_appender(dirs,infile_list):
    for filename in os.listdir(dirs):
        if filename.startswith("Orthogroups") and filename.endswith(".out"):
            infile_list.append(str(filename))

    return infile_list

def BEB(directory,infile):
    with open(os.path.join(directory,infile)) as f:
        beb_values = []
        for line in f:
            if "Bayes Empirical Bayes (BEB)" in line:
                remaining_lines = "".join(islice(f,None)).split("\n")
                for remaining_line in remaining_lines:
                    if "*" in remaining_line and "Positively" not in remaining_line:
                        beb_values.append(int(remaining_line.split()[0]))

    return beb_values


def model0_w(directory,infile):
    with open(os.path.join(directory,infile)) as f:
        w_site_classes = []
        for line in f:
            if "dN/dS (w) for site classes (K=3)" in line:
                remaining_lines = "".join(islice(f,None)).split("\n")
                for remaining_line in remaining_lines:
                    if "w:" in remaining_line:
                        w_site_classes.append(float(remaining_line.split()[3]))
    return w_site_classes

def model2_w(directory,infile):
    with open(os.path.join(directory,infile)) as f:
        fore_back_values = []
        for line in f:
            if "background w" in line:
                fore_back_values.append(float(line.split()[4]))
            if "foreground w" in line:
                fore_back_values.append(float(line.split()[4]))

    return fore_back_values



def dataframe_creator(fam_dict):
    df = pd.DataFrame.from_dict(fam_dict,orient="index")
    df = df.fillna(np.nan)

    return df


################################################################################


if args.m0:
    directory = sys.argv[2]
    csv_name = sys.argv[3]
    fam_dict = {}
    infiles = []
    infiles = infile_appender(directory,infiles)

    for infile in infiles:
        m0_w = model0_w(directory,infile)
        BEB_0 = BEB(directory,infile)
        fam_dict[infile.split(":")[0]] = [*m0_w,BEB_0]

    df = dataframe_creator(fam_dict)
    df.columns = ["model0_w","model0_BEB_sites"]
    df.to_csv("{}".format(csv_name),sep="\t")

elif args.m2:
    directory = sys.argv[2]
    csv_name = sys.argv[3]
    fam_dict = {}
    infiles = []
    infiles = infile_appender(directory,infiles)

    for infile in infiles:
        m2_w = model2_w(directory,infile)
        BEB_2 = BEB(directory,infile)
        fam_dict[infile.split(":")[0]] = [*m2_w,BEB_2]

    df = dataframe_creator(fam_dict)
    df.columns = ["background_w","foreground_w","model2_BEB_sites"]
    df.to_csv("{}".format(csv_name),sep="\t")

elif args.both:
    directory_1 = sys.argv[2]
    directory_2 = sys.argv[3]
    csv_name = sys.argv[4]
    fam_dict_1 = {}
    fam_dict_2 = {}

    infiles_1 = []
    infiles_2 = []
    infiles_1 = infile_appender(directory_1,infiles_1)
    infiles_2 = infile_appender(directory_2,infiles_2)


    for infile_1 in infiles_1:
        m0_w = model0_w(directory_1,infile_1)
        BEB_0 = BEB(directory_1,infile_1)
        fam_dict_1[infile_1.split(":")[0]] = [*m0_w,BEB_0]
    
    for infile_2 in infiles_2:
        m2_w = model2_w(directory_2,infile_2)
        BEB_2 = BEB(directory_2,infile_2)
        fam_dict_2[infile_2.split(":")[0]] = [*m2_w,BEB_2]

    df1 = pd.DataFrame.from_dict(fam_dict_1,orient="index")
    df1.columns = ["model0_w","model0_BEB_sites"]
    df2 = pd.DataFrame.from_dict(fam_dict_2,orient="index")
    df2.columns = ["background_w","foreground_w","model2_BEB_sites"]
    df = df1.join(df2)
    df.to_csv("{}".format(csv_name),sep="\t")
