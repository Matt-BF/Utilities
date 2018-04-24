rule write_ctl:
    input:
        "/codeml_model2_default.ctl"

    output:
        "/{folder}/comdel_model2.ctl"

    shell:
        "cp {input} {output} | sed #todo: find a way to add tree and aln to ctl"


rule codeml:
    input:
        "/{folder}/codeml_model2.ctl",
        "{folder}/{aln.fasta}",
        "/{folder}/{tree.nwk}"

    output:
        "/{folder}/{group}.{ext}"

    shell:
        "cd {folder} | codeml --group {wildcards.group} < {input} > {output}"
