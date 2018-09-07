from ete3 import EvolTree
import pickle
import sys

tree = EvolTree(newick=sys.argv[1],
                  binpath="/opt_hd/matt/Xuli/codeml_all_transp/")

fam_name = sys.argv[1].split(".")[2]

tree.link_to_alignment(sys.argv[2])
tree.workdir = "/opt_hd/matt/Xuli/codeml_all_transp/{}_codeml".format(fam_name)

for leaf in tree:
    if leaf.name.startswith("AFK"):
        tree.mark_tree([leaf.node_id], marks=["#1"])

for starting_omega in [0.2, 0.7, 1.2]:
    #model0
    tree.run_model("M0."+str(starting_omega),omega=starting_omega,NSsites="0 1 2")

    #branch-site tests
    tree.run_model("bsA."+str(starting_omega),omega=starting_omega)
    tree.run_model("bsA1."+str(starting_omega),omega=starting_omega)

with open("{}.pickle".format(fam_name),"wb") as f:
    pickle.dump(tree, f)
