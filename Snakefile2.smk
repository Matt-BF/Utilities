from Bio.Phylo.PAML import codeml
from pathlib import Path

########## create the lists ##########
folder = Path("./")

aln_list = []
tree_list = []

for infile in folder.iterdir():
    if infile.is_file() and str(infile).endswith("aln"):
        aln_list.append(str(infile))
    elif infile.is_file() and str(infile).endswith("treefile"):
        tree_list.append(str(infile))

######################################

rule all:
    input:
        expand("{align}", align="aln_list")
        expand("{tree}", tree="tree_list")  # add a file with newicks

rule model0:
    input:
        alignment_file = "{align}"
        tree_file = "{tree}"

    output:
        "{"{}_model0".format(str({align}).split(".")[2])}.out"

    run:
        cml0 = codeml.Codeml()
        cml0.set_options(noisy=9, verbose=1, runmode=0,
                         seqtype=1, CodonFreq=2, model=0, NSsites=[0, 1, 2],
                         ndata=1, icode=0, fix_kappa=0, kappa=2, fix_omega=0,
                         omega=0.2)
        cml0.alignment = {input.alignment_file}
        cml0.tree = {input.tree_file}
        cml0.out_file = {output}
        cml0.working_dir = "./"

        cml0.run()
