from Bio.Phylo.PAML import codeml


wildcard_constraints:
    folder = "fam\d+"

#ALN RULES
rule alignment:
    input:
        "{folder}/*.fasta"

    output:
        "{folder}/{folder}_aln_macse.fasta"

        shell:
            "macse line"

#TREE RULES
rule tree_infer:
    input:
        "{folder}/{folder}_aln_macse.fasta"

    output:
        "{folder}/{folder}_tree.nwk"

    threads: 4

    shell:
        "IQTree line"


#CODEML RULES
rule model0:

    input:
        "{folder}/{wildcards.aln}.aln",
        "{folder}/{wildcards.tree}.nwk"

    output:
        "{folder}/model0_results.out"

    run:
        cml0 = codeml.Codeml()
        cml0.set_options(noisy=9,verbose=1,runmode=0,
        seqtype=1,CodonFreq=2,model=0,NSsites=[0,1,2],
        ndata=1,icode=0,fix_kappa=0,kappa=2,fix_omega=0,
        omega=0.2)
        cml0.alignment = input[0]
        cml0.tree = input[1]
        cml0.out_file = output
        cml0.working_dir = {folder}

rule model2:

    input:
        "{folder}/{wildcards.aln}.aln",
        "{folder}/{wildcards.tree}_marked.nwk"

    output:
        "{folder}/model2_results.out"

    run:
        cml0 = codeml.Codeml()
        cml0.set_options(noisy=9,verbose=1,runmode=0,
        seqtype=1,CodonFreq=2,model=2,NSsites=2,
        ndata=1,icode=0,fix_kappa=0,kappa=2,fix_omega=0,
        omega=0.2)
        cml0.alignment = input[0]
        cml0.tree = input[1]
        cml0.out_file = output
        cml0.working_dir = {folder}
