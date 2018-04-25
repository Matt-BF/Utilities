wildcard_constraints:
    folder = "fam\d+"

rule write_ctl_0:
    input:
        "/codeml_model0_default.ctl"

    output:
        "/{folder}/model0/codeml_model0.ctl"

    shell:
        "cp {input} {output} | sed #todo: find a way to add tree and aln to ctl"


rule write_ctl_2:
    input:
        "/codeml_model2_default.ctl"

    output:
        "/{folder}/model2/codeml_model2.ctl"

    shell:
        "cp {input} {output} | sed #todo: find a way to add tree and aln to ctl"


rule codeml_0:
    input:
        "/{folder}/codeml_model0.ctl",

    output:
        "/{folder}/model0/{}.{ext}"

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
