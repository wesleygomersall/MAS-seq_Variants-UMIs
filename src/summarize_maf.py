#!/usr/bin/env python

from Bio import AlignIO
from collections import defaultdict
import argparse


def get_args():
  parser = argparse.ArgumentParser(description="A program to summarize maf files")
  parser.add_argument("-f", "--fasta", help="fasta file", required=True)
  parser.add_argument("-m", "--maf", help="input maf file", required=True)
  parser.add_argument("-o", "--output", help="output text file", required=True)
  return parser.parse_args()

args = get_args()


#mildly stolen from https://pynative.com/python-count-number-of-lines-in-file/
#generator used to keep from reading in the entire file, the fasta can be BIG
def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)
with open(args.output, 'w') as outFile:
  with open(args.fasta, 'rb') as fp:
      c_generator = _count_generator(fp.raw.read)
      # count each >	#modified
      count = sum(buffer.count(b'>') for buffer in c_generator)	#modified
      outFile.write(f"Total records: {count}\n")
  
  NUM_READS = count
  
  def defaultVal():
    return 0
  
  CR1_count = 0
  CR2_count = 0
  CR3_count = 0
  alnPerRead = defaultdict(defaultVal)  #key:read, value: count
  
  #was barcode01d-aln.maf
  for multipleAln in AlignIO.parse(args.maf, "maf"):
    alnPerRead[multipleAln[1].name] += 1
    match multipleAln[0].name:
      case "CR1":
        CR1_count += 1
      case "CR2":
        CR2_count += 1
      case "CR3":
        CR3_count += 1
  
  #print(f"CR1: {CR1_count}, CR2: {CR2_count}, CR3: {CR3_count}")
  outFile.write(f"CR1: {CR1_count}, CR2: {CR2_count}, CR3: {CR3_count}\n")
  
  
  options = set(alnPerRead.values())
  
  #print(f"0: {NUM_READS - len(alnPerRead)}, {(NUM_READS - len(alnPerRead)) / NUM_READS}")
  outFile.write(f"0: {NUM_READS - len(alnPerRead)}, {(NUM_READS - len(alnPerRead)) / NUM_READS}\n")

  for val in options:
    #print(f"{val}: {list(alnPerRead.values()).count(val)}, {list(alnPerRead.values()).count(val) / NUM_READS}")
    outFile.write(f"{val}: {list(alnPerRead.values()).count(val)}, {list(alnPerRead.values()).count(val) / NUM_READS}\n")

  
  #print(sorted(alnPerRead.items(), key=lambda item:item[1]))
