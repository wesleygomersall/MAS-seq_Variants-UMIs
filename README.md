# Mapping Barcodes to Genes with Long-Read Sequencing

Written by Wesley Gomersall, Mahmoud al Mahmoud, and Grace Hach for Dr. Calin Plesa

--------------------------------------

## Overview

This pipeline extracts paired gene and barcode sequences from long-read sequencing data produced from gene shuffling/protein engineering experiments in the Plesa Lab at the University of Oregon Knight Campus. It is designed to work with long read data in fastq format from PacBio MAS sequencing.

## Input Files 

- 1 BAM file containing CCS reads `*.ccs.bam`

In addition to the sequencing data, the pipeline requires files containing other sequences present in the DNA constructs:

- 1 FASTA file containing 3 conserved regions
    - with header lines "CR1", "CR2", and "CR3"
    - CR1 sequence should end with the ATG start codon.
- 1 FASTA file containing barcode sequences for demultiplexing, with barcode number indicated in the header lines.
- 1 FASTA file containing array barcodes for deconcatenating PacBio data using Skera

## Output Files

The primary output of the pipeline is a .csv file containing paired genes and barcodes. The columns contain:

- Barcode sequence
- Barcode count
- Consensus gene sequence
- Amino acid translation (to first stop codon)
- Amino acid translation (complete sequence)

Intermediate files are produced by each step of the pipeline. More details about outputs from each step are in /src/README.md.

## Options

`--infile`: Path to the raw FASTQ file. 

`--outdir`: Output directory for all results files. Will be populated with subfolders containing outputs for each process step. Default is `<current working directory>/results/<run start timestamp>-results`

`--crfile`: Path to FASTA file containing conserved region sequences.

`--arrfile`: Path to FASTA file containing MAS seq primer sequences. 

`--indexfile`: Path to FASTA file containing library indices.

`--length`: Maximum monomer length in nt. Default is 1200. Sequences longer than `length` will not be included in the analysis.

`--help`: Prints help information.

## Command

```
apptainer pull appimage.sif pb.def

$ /usr/bin/time -v nextflow run main.nf -with-apptainer pb_wkg.sif \
	--infile sequences/blue_test.bam \
	--arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta \
	--indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta \
	--crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/conserved_regions.fasta
```

This repo includes a file `pb.def` for building an apptainerimage. 
Build the image by running the following command in the project directory.

```
apptainer build <imagename>.sif pb.def
```

Utilizing the nextflow command `nextflow run main.nf -with-apptainer <imagename>.sif [OPTIONS]` allows the pipeline to run with this image.
In this case, options `--arrfile`, `--indexfile`, and `--crfile` must be located outside of the working directory (note: WIP).
Use full file paths for the command options.

This image was originally built for the Talapas High Performance Cluster at the University of Oregon in March of 2025.
For information about this image's intended OS, refer to the file pb.def

## Dependencies

The following programs are used in this pipeline. 
The pipeline may be ran in a conda environment with these dependencies without the apptainer image.

| Tool        | Version       |
| :---------- | ------------: |
| Nextflow    | 22.10.3       |
| Java        | 11 (up to 18) |
| Bash        | 3.2 or later  |
| Python      | 3.10          |
| matplotlib  | 3.7.1         |
| regex       | 2022.10.31    |
| Lima        | 2.7.1         |
| Skera       |               |
| Biopython   | 1.81          |
| bioawk      | 1.0           |
| LAST        | 1452          |
| lamassemble |               |
| starcode    | 1.4           |
| FastQC      |               |

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
