# Mapping Barcodes to Genes with Long-Read Sequencing

### Jacob Jensen, Beata Meluch, Keenan Raleigh, Dr. Calin Plesa
--------------------------------------

## Overview

This pipeline extracts paired gene and barcode sequences from long-read sequencing data produced from gene shuffling/protein engineering experiments in the Plesa Lab at the University of Oregon Knight Campus. It is designed to work with data from both Oxford Nanopore and PacBio sequencing platforms.

## Input Files

The expected input format depends on the sequencing platform.

For PacBio data: 

* 1 FASTQ file containing CCS reads (*.ccs.fastq)

For Oxford Nanopore data:

* Multiple FASTQ files containing demultiplexed sequencing data. (Tested on a set of 5 files)

In addition to the sequencing data, the pipeline requires files containing other sequences present in the DNA constructs:

* 1 FASTA file containing 3 conserved regions
    * with header lines "CR1", "CR2", "CR3"
    * CR1 sequence should end with the ATG start codon.
* 1 FASTA file containing barcode sequences for demultiplexing, with barcode number indicated in the header lines.


## Output Files

The primary output of the pipeline is a .tsv file containing paired genes and barcodes. The columns contain:

* Barcode sequence
* Barcode count
* Consensus gene sequence
* Amino acid translation (to first stop codon)
* Amino acid translation (complete sequence)

Intermediate files are produced by each step of the pipeline. More details about outputs from each step are in /src/README.md.


## Options

`--platform`: String specifying the sequencing platform origin of the data. Only accepts `pacbio` or `nanopore`. Defaults to `pacbio`.

`--infile`: Path to the raw FASTQ files. If sending multiple FASTQs at once (as for Oxford Nanopore data), use pattern matching to capture files. (e.g. `/folder/data/nanopore/barcode0*d_test.fastq`)

`--outdir`: Output directory for all results files. Will be populated with subfolders containing outputs for each process step. Default is `<current working directory>/results/<run start timestamp>-results`

`--crfile`: Path to FASTA file containing conserved region sequences.

`--indexfile`: Path to FASTA file containing library indices.

`--length`: Maximum monomer length in nt. Default is 1200. Sequences longer than `length` will not be included in the analysis.

`--help`: Prints help information.

## Notes

The location of starcode will need to be updated in the beginning of the script to reflect where it is installed in your local environment.


## Dependencies

| Tool        | Version       |
| :---------- | ------------: |
| Nextflow    | 22.10.3       |
| Java        | 11 (up to 18) |
| Bash        | 3.2 or later  |
| Python      | 3.10          |
| matplotlib  | 3.7.1         |
| regex       | 2022.10.31    |
| Lima        | 2.7.1         |
| Biopython   | 1.81          |
| bioawk      | 1.0           |
| LAST        | 1452          |
| lamassemble |               |
| starcode    | 1.4           |


## References

Starcode  
Filion, Guillaume. Starcode: Sequence clustering based on all-pairs search. Latest release: 02 Nov 2020. https://github.com/gui11aume/starcode

LAST  
Frith, Martin. last. Latest update: 17 Oct 2022. https://gitlab.com/mcfrith/last

Nextflow  
Seqera Labs. Nextflow. Latest release: 27 Oct 2022. https://github.com/nextflow-io/nextflow

lamassemble  
M. C. Frith, S. Mitsuhashi, K. Katoh, lamassemble: Multiple Alignment and Consensus Sequence of Long Reads. Methods Mol Biol 2231, 135-145 (2021). 

S. M. Karst, R. M. Ziels, R. H. Kirkegaard, E. A. Sørensen, D. McDonald, Q. Zhu, R. Knight, M. Albertsen, High-accuracy long-read amplicon sequences using unique molecular identifiers with Nanopore or PacBio sequencing. Nat Methods 18, 165–169 (2021).

Figures presented at Genomics in Action 2023 were created with Biorender. https://biorender.com/