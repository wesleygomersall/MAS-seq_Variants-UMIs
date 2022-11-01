#!/usr/bin/env python
from Bio import AlignIO
from Bio import SeqIO
from collections import defaultdict
import argparse

def get_args():
  parser = argparse.ArgumentParser(description="Extracts the barcodes and genes from fastqs based on records in a maf.")
  parser.add_argument("-f", "--fastq", help="ensembl mart file", required=True)
  parser.add_argument("-m", "--maf", help="FILTERED maf file associated with the input fastq", required=True)
  parser.add_argument("-c", "--counts", help="name for output text file with occurrence counts for barcodes", required=False)
  parser.add_argument("-o", "--out", help="output fasta file with id=fastq id, seq={20 base barcode}{gene}", required=True)
  return parser.parse_args()

args = get_args()

rawBarcodeLens = []
adjustedBarcodeLens = []

def defaultCount():
    return 0

rawBarcodesCounts = defaultdict(defaultCount)

#these would be used for adjusting the listed positions, but that didn't work as well as I hoped.
# realCR2 = "GGTACCTAAGTGTGGCTGCGGAAC"
# realCR3 = "GCACGACGTCAGGTGGCACTTTTCG"

# adjustedPositions = {} #key = {"end1", "start2", "end2", "start3"}, value = int
positions = {} #key = {"end1", "start2", "end2", "start3"}, value = int
reads = SeqIO.parse(args.fastq, "fastq")
currentRead = next(reads)
with open(args.out, "w") as outFile:
    for aln in AlignIO.parse(args.maf, "maf"):
        while aln[1].name != currentRead.name:
            currentRead = next(reads)
        if len(positions) < 4:
            match aln[0].name:
                case "CR1":
                    # adjustedPositions["end1"] = aln[1].annotations["start"] + aln[1].annotations["size"]#pos+len
                    positions["end1"] = aln[1].annotations["start"] + aln[1].annotations["size"]#pos+len
                case "CR2":
                    # adjustedPositions["start2"] = aln[1].annotations["start"] - realCR2.find(str(aln[0].seq))
                    positions["start2"] = aln[1].annotations["start"]
                    # adjustedPositions["end2"] = aln[1].annotations["start"] + aln[1].annotations["size"] + realCR2[::-1].find(str(aln[0].seq)[::-1])#pos+len
                    positions["end2"] = aln[1].annotations["start"] + aln[1].annotations["size"] #pos+len
                case "CR3":
                    # adjustedPositions["start3"] = aln[1].annotations["start"] - realCR3.find(str(aln[0].seq))
                    positions["start3"] = aln[1].annotations["start"]
        if len(positions) == 4: #if all 3 regions have been parsed in the maf file
            # adjustedBarcodeLens.append(adjustedPositions["start3"] - adjustedPositions["end2"])
            rawBarcodeLens.append(positions["start3"] - positions["end2"])
            if aln[1].annotations["strand"] == 1:
                rawBarcode = str(currentRead.seq)[positions["end2"]:positions["start3"]]
                rawGene = str(currentRead.seq)[positions["end1"]-3:positions["start2"]]
            else:
                rawBarcode = str(currentRead.reverse_complement().seq)[positions["end2"]:positions["start3"]]
                rawGene = str(currentRead.reverse_complement().seq)[positions["end1"]-3:positions["start2"]]
#             if (positions["start3"] - positions["end2"]) >= 15 and (positions["start3"] - positions["end2"]) <= 25:
            if (positions["start3"] - positions["end2"]) == 20:
                rawBarcodesCounts[rawBarcode] += 1
                outFile.write(f">{currentRead.id}\n{rawBarcode}{rawGene}\n")
                
            positions.clear()
            # adjustedPositions.clear()

print(min(rawBarcodeLens))
print(max(rawBarcodeLens))
print(sum(rawBarcodeLens) / len(rawBarcodeLens))

if args.counts:
    with open(args.counts, "w") as outFile:
        sortedBarcodeCounts = sorted(rawBarcodesCounts.items(), key=lambda item: item[1], reverse=True)
        outFile.write("Barcode\tCount\n")
        for barcode, count in sortedBarcodeCounts:
            outFile.write(f"{barcode}\t{count}\n")