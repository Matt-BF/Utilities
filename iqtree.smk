import glob


aln_list = glob.glob('./*.aln')
print(aln_list)


rule IQTree:
	input:
		expand("{align}", align=[aln_list])

	output:
		"{align}.out"

	threads: 10:

	shell:
		"/opt_hd/matt/softwares/iqtree-1.6.5-Linux/bin/iqtree -s {input} -nt AUTO"