#!/usr/bin/env python

import argparse
import Bio
from Bio.Seq import Seq
import re

def get_args():
    parser = argparse.ArgumentParser(description="This script will create the output format that we want from the whole pipeline")
    parser.add_argument("-f", help="Fasta file containing the consensussed barcode clusters", type=str, required = True)
    parser.add_argument("-o", help="output file", type=str, required = True)
    return parser.parse_args()

parameters = get_args()
f = parameters.f
o = parameters.o

#to make a protein someday
# def make_protein(seq):
#     a = seq.translate()
#     for n,p in enumerate(a):
#         if p == "M":
#             start = n
#         if p =="\*":
#             stop = n
#             prot = a[start:stop]
#             return (prot)


with open (f, "r") as fin, open (o,"w") as oout:
    while True:                                                 #the while loop will allow me to close the loop wherever in the script I need to
        line = fin.readline().strip()
        if line == "":                                          #finds the end of the file
            break                                               #ends the loop
        if line [0] == ">":
            barcode = re.findall("[AGTC]+",line)[0]
            count = re.findall("\d+",line)[0]
            line = fin.readline().strip()
            sequence = Seq(line)
        rna_seq = sequence.transcribe()
        translation =  rna_seq.translate(to_stop=True)
        translation2 =  rna_seq.translate()
        #protein = make_protein(sequence)
        #print (barcode,"\t",count, "\t", sequence,"\t", translation,"\t", translation2, "\t",f,sep = "", file = oout)
        print (barcode, count, sequence, translation, translation2, f, sep = ",", file = oout)