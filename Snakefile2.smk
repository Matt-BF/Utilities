from Bio.Phylo.PAML import codeml

wildcard_constraints:
    folder = "fam\d+"

#CODEML PIPELINE


rule write_ctl_0:
    input:
        "/codeml_model0_default.ctl"

    output:
        "/{folder}/model0/codeml_model0.ctl"

    shell:
        "cp {input} {output} |\
         sed -i "s/seqfile = /seqfile = [aln]" {output} |\
         sed -i "s/treefile = /treefile = [tree]" {output} |\
         sed -i "s/outfile = /outfile = ./{folder}_paml_model0"


rule write_ctl_2:
    input:
        "/codeml_model2_default.ctl"

    output:
        "/{folder}/model2/codeml_model2.ctl"

    shell:
        "cp {input} {output} |\
         sed -i "s/seqfile = /seqfile = [aln]" {output} |\
         sed -i "s/treefile = /treefile = [tree]" {output} |\
         sed -i "s/outfile = /outfile = ./{folder}_paml_model2"


rule codeml_0:
    input:
        "/{folder}/codeml_model0.ctl",

    output:
        "/{folder}/model0/{file}.{ext}"

    shell:
        "cd {folder} | codeml {codeml.input} > {output}"


rule codeml_2:
    input:
        "/{folder}/codeml_model2.ctl",

    output:
        "/{folder}/model2/{file}.{ext}"

    shell:
        "cd {folder} | codeml {codeml.input} > {output}"

#TODO: add config file with directory, tree and aln
