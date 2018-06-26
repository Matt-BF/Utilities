import glob

aln_list = glob.glob('*.aln')


rule all:
    input:
        expand("{alignment}.out", alignment=aln_list)

rule IQTree:
    input: "{sample}"
    output: "{sample}.out"
    shell:
        "/opt_hd/matt/softwares/iqtree-1.6.5-Linux/bin/iqtree -s {input} -nt 3"
