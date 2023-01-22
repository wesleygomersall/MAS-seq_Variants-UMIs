#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="This script will create the quality bins for the various barcodes")
    parser.add_argument("-lib5", help="tab seperated file with the library 5 final output", type=str, required = True)
    parser.add_argument("-lib4", help="tab seperated file with the library 4 final output", type=str, required = True)
    parser.add_argument("-o", help="output file", type=str, required = True)
    return parser.parse_args()

parameters = get_args()
l5 = parameters.lib5
l4 = parameters.lib4
o = parameters.o

lib4_dict = {}
lib5_dict = {}

def fill_dict (lib,dict):
    with open (lib, "r") as l:
        while True:
            line = l.readline().strip()
            if line == "":
                break
            line = line.split()
            barcode = line[0]
            dict[barcode] = (line[1])
        return dict

fill_dict(l5,lib5_dict)
fill_dict(l4,lib4_dict)

qual_5 = {}
qual_4 = {}
qual_3 = {}
qual_2 = {}
qual_1 = {}

l5_count = 0
l4_count = 0
l3_count = 0
l2_count = 0
l1_count = 0


total = 0

for barcodes in lib5_dict:
    #incriments through lib5
    if barcodes in lib4_dict:
        #checks if the barcode is in both libraries
        total+=1
        #adds one to the total for the barcode being present in both libraries
        l5_count = int(lib5_dict[barcodes])
        l4_count = int(lib4_dict[barcodes])
        if l5_count > 1 and l4_count >1:
            qual_1[barcodes] = (("lib4",l4_count),("lib5",l5_count))
        if l5_count >= 1 or l4_count >= 1:
            qual_2[barcodes] = (("lib4",l4_count),("lib5",l5_count))
        if l5_count >= 1 and l4_count >= 1:
            qual_4[barcodes] = (("lib4",l4_count),("lib5",l5_count))
    else:
        total +=1
        l5_count = int(lib5_dict[barcodes])
        if l5_count >1:
            qual_3[barcodes] = ("lib5",l5_count)
            qual_4[barcodes] = ("lib5",l5_count)
        else:
            qual_5[barcodes] = ("lib5",l5_count)

for barcodes in lib4_dict:
    #incriments through lib4
    if barcodes not in lib5_dict:
        total+=1
    # if barcodes not in qual_1 or barcodes not in qual_2:
        l4_count = int(lib4_dict[barcodes])
        if l4_count >1:
            qual_3[barcodes] = ("lib4",l4_count)
            qual_4[barcodes] = ("lib5",l5_count)
        else:
            qual_5[barcodes] = ("lib4",l4_count)

with open (o,"w") as oout:
    print ("Present in both blue libraries, with multiple barcodes", len(qual_1),file = oout)
    print ("Present in both blue libraries", len(qual_2),file = oout)
    print ("Multiple barcodes, only one blue library", len(qual_3),file = oout)
    print ("Either multiple barcodes or both blue libraries", len(qual_4),file = oout)
    print ("Single barcode, single blue library", len(qual_5),file = oout)
    print ("total", total,file = oout)
    print (len(qual_4) + len(qual_5),file = oout)

