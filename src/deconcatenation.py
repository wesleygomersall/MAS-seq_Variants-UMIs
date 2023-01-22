#!/usr/bin/env python

# Adapted from Calin's deconcatenation script

from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import regex
import argparse

#################### FUNCTION DEFINITIONS ####################

def get_filenames() -> tuple:
    """Parses filename arguments"""
    parser = argparse.ArgumentParser(description="Get file paths for input CCS FASTQ file and output monomer FASTQ file.")
    parser.add_argument("-f", "--file", help="Absolute path to input CCS file", required=True)
    parser.add_argument("-o", "--output", help="Output monomer filename", required=True)
    parser.add_argument("-s", "--sequences", help="FASTA filename containing sequences of conserved regions and library indices", required=True)
    args = parser.parse_args()
    return args.file, args.output, args.sequences


def get_sequences(fname: str) -> tuple:
    """Takes filename of FASTA containing conserved regions and library indices.
    Returns a tuple containing a dictionary of conserved regions
    and a dictionary of library indices."""
    conserved_regions: dict = {}   
    index_fwd: dict = {}

    for seq_record in SeqIO.parse(fname, "fasta"):
        for i in ("CR", "conserved", "conserved_region"):
            if i in seq_record.id:
                conserved_regions[seq_record.id] = str(seq_record.seq)
        for j in ("index", "barcode"):
            if j in seq_record.id:
                index_fwd[seq_record.id] = str(seq_record.seq)
    return conserved_regions, index_fwd


def find_monomers(seq_record, conserved_regions: dict) -> tuple:
    """
    Looks for CRs as defined in the input FASTA. In this implementation,
    [reverse complement of first 24 nt of CR1, last 24nt of CR3]
    Returns: sequence before first sep, the rest of the sequence
    """
    sequence: Seq = seq_record.seq  # pull Seq object out of SeqRecord object
    all_hits: list = []
    reg_hits: list = []

    index_length: int = 24      # default index length
    con_length: int = 24        # default conserved region length, updates on match

    # if the read is less than 20 nt, return the record object as the monomer and nothing as the remainder
    if len(sequence) < 20:
        return seq_record, ''

    else:
        for i in conserved_regions.values():     # 2 iterations
            cr: str = i.upper()
            motif = r"("+cr+r"){e<2}"   # two allowed errors of any type: insertion, deletion, substitution
            match = regex.search(motif, str(sequence), regex.BESTMATCH)     # search returns 1st match object

            if match:
                list_matches = match.start()                                # returns location of 1st match
                all_hits.append(list_matches)                               # all_hits stores location of match
                reg_hits.append(match.start(0))                             # reg_hits stores match object
                #print('Added '+str(list_matches)+' for '+cr+' and '+str(match.start(0))+' for regex')
                con_length = len(cr)
            
        if all_hits == []:
            #print('no conserved region found')
            return seq_record, ''
        else:
            #lowest_index = min(all_hits)
            lowest_index = min(reg_hits)
            #print('chose position '+str(lowest_index))
            
            # slicing is acting on the SeqRecord object
            if len(seq_record) > lowest_index+con_length+index_length+1:
                monomer = seq_record[:lowest_index+con_length+index_length]
                sequence = seq_record[lowest_index+con_length+index_length:]
            else:
                monomer = seq_record[:]
                sequence = ''
            return monomer, sequence


#################### SCRIPT ####################

inpath, outfile, inseq = get_filenames()

# extract CR and index sequences
conserved_regions, index_fwd = get_sequences(inseq)

counter: int = 0    # count monomers per read

with open(outfile, 'w') as output:
    for seq_record in SeqIO.parse(inpath, "fastq"):
        counter = 0
        # while there is remaining sequence as we move through the record
        while seq_record:
            # extract current monomer and remainder of current record
            monomer, seq_record = find_monomers(seq_record, conserved_regions)

            if len(monomer.seq) > 44 and len(monomer.seq) < 100000:
                # add count for unique deconcatenated read IDs
                monomer.id = monomer.id+"_"+str(counter)
                monomer.description = monomer.description+"_"+str(counter)
                counter += 1
                SeqIO.write(monomer, output, "fastq")