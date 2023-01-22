#!/usr/bin/env python
from Bio import AlignIO
from Bio import SeqIO
from collections import defaultdict
import argparse

def get_args():
  parser = argparse.ArgumentParser(description="Extracts the barcodes and genes from fastqs based on records in a maf.")
  parser.add_argument("-f", "--fasta", help="fasta input used for alignment", required=True)
  parser.add_argument("-m", "--maf", help="FILTERED maf file associated with the input fastq", required=True)
  parser.add_argument("-o", "--outBase", help="output basename. For example: 'lib1' would create 'lib1_barcodes.fasta', 'lib1_genes.fasta', 'lib1_concat.fasta', 'lib1_counts.tsv', and 'lib1_dist.tsv'", required=True)
  return parser.parse_args()

args = get_args()

barcodeFile = f"{args.outBase}_barcodes.fasta"
geneFile = f"{args.outBase}_genes.fasta"
concatFile = f"{args.outBase}_concat.fasta"
countFile = f"{args.outBase}_counts.tsv"
distFile = f"{args.outBase}_dist.tsv"

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
reads = SeqIO.parse(args.fasta, "fasta")
currentRead = next(reads)
print("Started...")
progressCount = 0
with open(concatFile, "w") as concatFileOut, open(barcodeFile, "w") as barcodeFileOut, open(geneFile, "w") as geneFileOut:
    for aln in AlignIO.parse(args.maf, "maf"):
        while aln[1].name != currentRead.name:
            #this runs once for each line of the fastq
            currentRead = next(reads)
            progressCount += 1 
            if progressCount % 5000 == 0:
                print(f"Processed {progressCount} reads.")
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
            if (positions["start3"] - positions["end2"]) <= 21 and (positions["start3"] - positions["end2"]) >= 19:
                rawBarcodesCounts[rawBarcode] += 1
                concatFileOut.write(f">{currentRead.id}\n{rawBarcode}{rawGene}\n")
                barcodeFileOut.write(f">{currentRead.id}\n{rawBarcode}\n")
                geneFileOut.write(f">{currentRead.id}\n{rawGene}\n")
                
            positions.clear()
            # adjustedPositions.clear()

print(min(rawBarcodeLens))
print(max(rawBarcodeLens))
print(sum(rawBarcodeLens) / len(rawBarcodeLens))

countDistribution = {}
with open(countFile, "w") as outFile:
    sortedBarcodeCounts = sorted(rawBarcodesCounts.items(), key=lambda item: item[1], reverse=True)
    outFile.write("Barcode\tCount\n")
    for barcode, count in sortedBarcodeCounts:
        outFile.write(f"{barcode}\t{count}\n")
        if count not in countDistribution:
            countDistribution[count] = 1
        else:
            countDistribution[count] += 1

with open(distFile, "w") as outFile:
    outFile.write("Number of reads with the same barcode\tCount\n")
    for readCount, timesItHappened in countDistribution.items():
        outFile.write(f"{readCount}\t{timesItHappened}\n")
