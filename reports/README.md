# Additional Analyses and Reports

This folder contains information about analyses done on the PacBio and Oxford Nanopore sequencing data outside of the immediate pipeline output.

## Contents

`/confidence_bins/` contains the output of `/src/confidence_bins.py`. These are text files containing counts of sequences falling into each confidence category (see the `/src/` README for details.) 
There are three text files - one for Oxford Nanopore data, one for Pacbio data, and one that was generated using the output from Dr. Plesa's original workflow on the Pacbio data (following the steps shared in the OneNote document).
The "Blank seqs" datapoint is a count of the number of blank protein sequences (see `Final_Output_Notes.md - Gaps in lamassemble Output`).

`Final_Output_Notes.md` contains commentary on certain pipeline steps and the final output of the pipeline.

