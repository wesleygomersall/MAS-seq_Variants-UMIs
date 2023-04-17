#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Get library 4 and 5 files for barcode-gene pair confidence binning")
    parser.add_argument("-lib4", help="CSV file with the library 4 final output", type=str, required = True)
    parser.add_argument("-lib5", help="CSV file with the library 5 final output", type=str, required = True)
    parser.add_argument("-o", help="output file", type=str, required = True)
    return parser.parse_args()

parameters = get_args()
lib4_path: str = parameters.lib4
lib5_path: str = parameters.lib5
output_path: str = parameters.o

def fill_dict (lib_path: str) -> tuple:
    """Populates a dictionary with barcode-gene pairs from one library.
    Protein seqs are keys, values are tuples of barcodes."""
    d: dict = {}
    blank_count: int = 0
    with open (lib_path, "r") as lib_file:
        #lib_file.readline()
        for line in lib_file:
            pair_items = line.strip().split(',')
            barcode = pair_items[0]
            protseq = pair_items[3]

            if protseq == "":
                blank_count += 1
            else:
                if protseq in d:
                    d[protseq] = (d[protseq]) + (barcode,)
                else:
                    d[protseq] = (barcode,)
            # if len(d) == 10:
            #     print(d)

    return d, blank_count

lib4_dict, lib4_blank_count = fill_dict(lib4_path)
lib5_dict, lib5_blank_count = fill_dict(lib5_path)

conf1: dict = {}
conf2: dict = {}
conf3: dict = {}
conf4: dict = {}
conf5: dict = {}

total = 0

for protseq in lib5_dict:
    if protseq in lib4_dict: # present in both libraries - option 1 2 3 4
        total += 1
        if len(lib4_dict[protseq]) > 1: # multiple barcodes lib4

            if len(lib5_dict[protseq]) > 1: # multiple barcodes, both libraries
                conf1[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf2[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf3[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf4[protseq] = (lib4_dict[protseq], lib5_dict[protseq])

            else: # multiple barcodes Lib4, only one barcode Lib5
                conf2[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf3[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf4[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
            
        else: # only one barcode lib4
            if len(lib5_dict[protseq]) > 1: # only one barcode lib4, multiple barcodes lib5
                conf2[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf3[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf4[protseq] = (lib4_dict[protseq], lib5_dict[protseq])

            else: # only one barcode in both libraries
                conf2[protseq] = (lib4_dict[protseq], lib5_dict[protseq])
                conf4[protseq] = (lib4_dict[protseq], lib5_dict[protseq])

    else: # present in only lib5 - options 3 4 5
        total += 1
        if len(lib5_dict[protseq]) > 1: # multiple barcodes only lib 5
            conf3[protseq] = lib5_dict[protseq]
            conf4[protseq] = lib5_dict[protseq]

        else: # only one barcode, only lib5
            conf5[protseq] = lib5_dict[protseq]

for protseq in lib4_dict:
    if protseq not in lib5_dict: # present in only lib4 - options 3 4 5
        total+=1
        if len(lib4_dict[protseq]) > 1: # multiple barcodes only lib 4
            conf3[protseq] = lib4_dict[protseq]
            conf4[protseq] = lib4_dict[protseq]

        else: # only one barcode, only lib4
            conf5[protseq] = lib4_dict[protseq]

with open (output_path, "w") as outfile:
    print ("Confidence Level 1: Present in both blue libraries, with multiple barcodes: ", len(conf1), file = outfile)
    print ("Confidence Level 2: Present in both blue libraries: ", len(conf2), file = outfile)
    print ("Confidence Level 3: Present in at least one blue library, with multiple barcodes: ", len(conf3), file = outfile)
    print ("Confidence Level 4: Present in both blue libraries and/or has multiple barcodes: ", len(conf4), file = outfile)
    print ("Confidence Level 5: Present in only one blue library, with only one barcode: ", len(conf5), file = outfile)
    print ("Total pairs evaluated: ", total,file = outfile)
    print ("Sum of Level 4 and Level 5: ", len(conf4) + len(conf5), file = outfile)
    print ("\nBlank seqs in Library 4: ", lib4_blank_count, file = outfile)
    print ("Blank seqs in Library 5: ", lib5_blank_count, file = outfile)