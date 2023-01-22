#!/usr/bin/env python

from Bio import AlignIO
import argparse

def get_args():
  parser = argparse.ArgumentParser(description="A program to keep maf records for reads which exactly have the CR1, CR2, andCR3 regions.")
  parser.add_argument("-i", "--inFile", help="input maf file", required=False)
  parser.add_argument("-o", "--outFile", help="output maf file", required=False)
  return parser.parse_args()

args = get_args()

storage = []
regions = set()
directions = set()
readName = ""
with open(args.outFile, "w") as outFile:
    for aln in AlignIO.parse(args.inFile, "maf"):
        if readName == "":
            readName = aln[1].name
        if readName != aln[1].name:
            if len(storage) == 3:
                if regions == {"CR1", "CR2", "CR3"}:
                    if len(directions) == 1:
                        AlignIO.write(storage, outFile, "maf")
                        storage.clear()
                        regions.clear()
                        directions.clear()
            else:
                storage.clear()
                regions.clear()
                directions.clear()
            readName = aln[1].name
        regions.add(aln[0].name)
        storage.append(aln)
        directions.add(aln[1].annotations["strand"])
    if len(storage) == 3:
        if regions == {"CR1", "CR2", "CR3"}:
            if len(directions) == 1:
                AlignIO.write(storage, outFile, "maf")
                storage.clear()
                regions.clear()
                directions.clear()
    else:
        storage.clear()
        regions.clear()
        directions.clear()
