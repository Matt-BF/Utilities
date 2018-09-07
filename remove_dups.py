from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys
import argparse

parser = argparse.ArgumentParser(description="remove duplicates from a FASTA file inplace")
parser.add_argument("fname", help="FASTA file")
args = parser.parse_args()

if args.fname:
    fname = sys.argv[1]
else:
    print("no FASTA file given")

with open(fname) as f:
    seqs = list(SeqIO.parse(f,"fasta"))
    
no_dup = {seq.id:seq for seq in seqs}

with open(fname,"w") as j:
    SeqIO.write([SeqRecord(sequence.seq,sequence.id,"","") for key,sequence in no_dup.items()],j,"fasta")
