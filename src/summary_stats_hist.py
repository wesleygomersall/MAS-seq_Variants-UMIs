#!/usr/bin/env python

import matplotlib.pyplot as plt
import argparse
import numpy as np
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from collections import Counter

def get_filenames() -> tuple:
    """Parses input and output file information"""
    parser = argparse.ArgumentParser(description="Get path of FASTX file.")
    parser.add_argument("-f", "--infile", help="Absolute path to input FASTX file", type=str, required=True)
    parser.add_argument("-o", "--outname", help="Name of output file and plot title", type=str, required = True)
    parser.add_argument("-t", "--filetype", help="Specify fasta or fastq", type = str, default = "fastq")
    args = parser.parse_args()
    return args.infile, args.outname, args.filetype

inpath, outname, filetype = get_filenames()
outpath: str = outname+".txt"

# Save read lengths as a list
read_lengths: list = []
for record in SeqIO.parse(inpath, filetype):
    read_lengths.append(len(record.seq))

# Create a dictionary with keys = lengths, values = counts
binned_read_lengths = Counter(read_lengths)

# Write out read length statistics
with open(outpath, "w") as outfile:
    outfile.write(f"Records in file: {len(read_lengths)}\n")
    outfile.write(f"Read lengths:\n")
    outfile.write(f"\t Minimum: {np.min(read_lengths)}\n")
    outfile.write(f"\t Maximum: {np.max(read_lengths)}\n")
    outfile.write(f"\t Average: {np.mean(read_lengths)}\n")
    outfile.write(f"\t Median: {np.median(read_lengths)}\n")
    outfile.write(f"\t Stdev: {np.std(read_lengths)}\n")

# Generate read length histogram
plt.title(outname)
plt.xlabel("Read length")
plt.ylabel("Count")
plt.bar(binned_read_lengths.keys(), binned_read_lengths.values(), width=20)
plt.savefig(outname.replace(" ","")+".png")
plt.show()