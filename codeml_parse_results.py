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

def infile_appender(dirs,num,infile_list):
    for filename in os.listdir(dirs.split()[num]):
        if filename.endswith(".out"):
            infile_list.append(str(filename))

    return infile_list

def BEB(infile):
    with open(os.path.join(directory,infile)) as f:
        beb_values = []
        for line in f:
            if "Bayes Empirical Bayes (BEB)" in line:
                remaining_lines = "".join(islice(f,None)).split("\n")
                for remaining_line in remaining_lines:
                    if "*" in remaining_line:
                        beb_values.append(int(remaining_line.split()[0]))
        if len(beb_values)<1:
            beb_values = np.nan

    return beb_values


def model0_w(infile):
    with open(os.path.join(directory,infile)) as f:
        w_site_classes = []
        for line in f:
            if "dN/dS (w) for site classes (K=3)" in line:
                remaining_lines = "".join(islice(f,None)).split("\n")
                for remaining_line in remaining_lines:
                    if "w:" in remaining_line:
                        w_site_classes.append(float(remaining_line.split()[3]))
    return w_site_classes

def model2_w(infile):
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

directory = sys.argv[2]
csv_name = sys.argv[3]



if args.m0:
    fam_dict = {}
    if len(directory.split())==1:
        infiles = []
        infiles = infile_appender(directory,0,infiles)
    else:
        print("Incorrect number of directories (pass 1 or 2 directories)")
        sys.exit()

    for infile in infiles:
        m0_w = model0_w(infile)
        BEB_0 = BEB(infile)
        fam_dict[infile.split(":")[0]] = [*model0_w(infile),BEB(infile)]

    df = dataframe_creator(fam_dict)
    df.columns = ["model0_w","model0_BEB_sites"]
    df.to_ ("{}.csv".format(csv_name),sep="\t")

elif args.m2:
    fam_dict = {}
    if len(directory.split())==1:
        infiles = []
        infiles = infile_appender(directory,0,infiles)
    else:
        print("Incorrect number of directories (pass 1 or 2 directories)")
        sys.exit()

    for infile in infiles:
        m2_w = model2_w(infile)
        BEB_2 = BEB(infile)
        fam_dict[infile.split(":")[0]] = [*m2_w,BEB_2]

    df = dataframe_creator(fam_dict)
    df.columns = ["background_w","foreground_w","model2_BEB_sites"]
    df.to_csv("{}.csv".format(csv_name),sep="\t")

elif args.both:
    fam_dict_1 = {}
    fam_dict_2 = {}

    if len(directory.split())==2:
        infiles_1 = []
        infiles_2 = []
        infiles_1 = infile_appender(directory,0,infiles_1)
        infiles_2 = infile_appender(directory,0,infiles_2)

    else:
        print("Incorrect number of directories (pass 1 or 2 directories)")
        sys.exit()

    for infile in infiles_1:
        m0_w = model0_w(infile)
        m2_w = model2_w(infile)
        BEB_0 = BEB(infile)
        BEB_2 = BEB(infile)
        fam_dict_1[infile.split(":")[0]] = [*m0_w(infile),BEB(infile)]
    for infile in infiles_2:
        fam_dict_2[infile.split(":")[0]] = [*m2_w(infile),BEB(infile)]

    df1 = pd.Dataframe_from_dict(fam_dict_1,orient="index")
    df2 = pd.Dataframe_from_dict(fam_dict_2,orient="index")
    df = df1.join(df2)
    df.columns = ["model0_w","model0_BEB_sites","background_w",
    "foreground_w","model2_BEB_sites"]
    df.to_csv("{}.csv".format(csv_name),sep="\t")
