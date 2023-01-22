#!/usr/bin/env python
from Bio import SeqIO
import argparse
import subprocess
from re import search

def get_args():
  parser = argparse.ArgumentParser(description="Extracts the variable region sequences for each barcode cluster")
  parser.add_argument("-f", "--fasta", help="fasta to pull variable region sequences from", required=True)
  parser.add_argument("-s", "--starcodedBarcodes", 
    help="output file from starcode showing clusters (use all the output options when running starcode)", required=True)
  parser.add_argument("-o", "--output", help="fasta to create with consensus sequences")
  parser.add_argument("-t", "--tempFile", help="fasta that will hold temporary results. Do not start multiple runs in the same directory with the same tempFile")
  return parser.parse_args()

args = get_args()

#just in case it already exists, appending happens every else
subprocess.run(f"rm {args.output}", shell=True)

with open(args.starcodedBarcodes) as SBFile:
	for i, clusterEntry in enumerate(SBFile):
		clusterEntry = clusterEntry.strip().split()
		barcode = clusterEntry[0]
		print(barcode)
		indexes = [int(value) for value in clusterEntry[3].split(",")]
		#print(indexes)

		if len(indexes) == 1:
			#read through remainder of 1 count lines (they are sorted! YAY!)
			print("getting singletons")
			onlyOneIndexList = []
			onlyOneIndexList.append(indexes[0])
			for line in SBFile:
				clusterEntry = line.strip().split()
				print(clusterEntry)
				barcode = clusterEntry[0]
				indexes = [int(value) for value in clusterEntry[3].split(",")]
				onlyOneIndexList.append(indexes[0])
			keepRecords = []
			with open(args.fasta) as fastaInFile:
				for j, record in enumerate(SeqIO.parse(fastaInFile, "fasta")):
					if j > indexes[-1]:
						break
					if j in onlyOneIndexList:
						record.id = f"{barcode}_1"
						record.description = record.id
						keepRecords.append(record)
			with open(args.output, "a") as outFile:
				SeqIO.write(keepRecords, outFile, "fasta-2line")
			break

		keepRecords = []
		with open(args.fasta) as fastaInFile:
			for j, record in enumerate(SeqIO.parse(fastaInFile, "fasta")):
				#print(j)
				if j > indexes[-1]:
					#print(j)
					#print(indexes[-1])
					break
				if j in indexes:
					#print(j)
					keepRecords.append(record)
			with open(args.tempFile, 'w') as outFile:
				#print("outputting")
				SeqIO.write(keepRecords, outFile, "fasta-2line")
		#break
		
		result = subprocess.run(f"lamassemble -n {barcode}_{len(indexes)} /projects/bgmp/jjensen7/promethion.mat {args.tempFile} >> {args.output}", capture_output=True, text=True, shell=True)
		print(result.stderr)
		if result.stderr != "":
			regexResult = search(r"(\d+) out of (\d+) sequences", result.stderr)
			#print(f"{regexResult.group(1)} out of {regexResult.group(2)}")
		
		#break
		subprocess.run(f"rm {args.tempFile}", shell=True)

		#if i >= 50:
		#	break
