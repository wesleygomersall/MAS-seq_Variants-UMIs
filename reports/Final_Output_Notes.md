# Final Pipeline Output

### Jacob Jensen, Beata Meluch, Keenan Raleigh
--------------------------------------

## Pipeline Resource Usage

### Pacbio Data

* Libraries 1, 2, 4, and 5 had final output .csv files roughly 2 hours after starting the run. The 6-hour runtime was due to the size of Library 3.

#### SLURM Output
```
    Command being timed: "../../nextflow/nextflow main.nf --platform pacbio --infile /projects/bgmp/shared/groups/2022/SKU/plesa/uploads/data/pacbio_raw/5664/ccs.Q20/m64047_220402_055906.ccs.fastq --outdir results/pacbio_full_dataset"
	User time (seconds): 26439.97
	System time (seconds): 12974.63
	Percent of CPU this job got: 183%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 5:57:41
```
#### Nextflow Output
```
	Duration    : 5h 57m 40s
	CPU hours   : 12.6
```

### Oxford Nanopore Data

* Libraries 1, 2, 4, and 5 had final output .csv files within 3 hours after starting the run. The 11-hour runtime was due to the size of Library 3.

#### SLURM Output
```
	Command being timed: "../../nextflow/nextflow main.nf --platform nanopore --infile /projects/bgmp/shared/groups/2022/SKU/plesa/uploads/data/nanopore_raw/barcode0*d.fastq --outdir results/nanopore_full_dataset"
	User time (seconds): 43410.85
	System time (seconds): 16268.06
	Percent of CPU this job got: 152%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 10:50:47
```
#### Nextflow Output
```
    Duration    : 10h 50m 46s
    CPU hours   : 16.2
```


## Barcode Collisions and lamassemble

By design, lamassemble looks for pairwise similarities within a cluster, and excludes divergent sequences from the group of sequences used to create the consensus.

Here is some example output from our `runLamassemble.py` script (step 8 of the Nextflow pipeline, output is saved in `.command.out` in the corresponding Nextflow work directory):

```
From Nanopore Library 3

ATTACCTTCCTTTGAGTAAT
[10225, ..., 1727401]
lamassemble: using 357 out of 379 sequences (linked by pairwise alignments)

ATGCCGAGTGTTACAGAGTA
[20974, ..., 1726152]
lamassemble: using 245 out of 286 sequences (linked by pairwise alignments)

CACACCCTGTCGGCAGTAAA
[13997, ..., 1731940]
lamassemble: using 196 out of 243 sequences (linked by pairwise alignments)
```

Clusters with highly divergent sequences will say "using 1 out of x sequences" and produce no consensus sequence, leaving a blank in the final output .csv.

This is a rough way of approaching barcode collisions. lamassemble will still produce a consensus sequence from a very small proportion of sequences that are found to be similar. One way of refining this method of detection might be to capture the warning message output and implement a cutoff (e.g. 80% of the reads in the cluster must be used in the consensus sequence, or the cluster is considered to have a collision).

### Gaps in lamassemble Output

As mentioned above, if lamassemble finds no similarities in a cluster, a consensus sequence is not produced. This leaves a gap in the final output .csv:

```
Pacbio Library 1
source file: m64047_220402_055906.ccs.0--0-final.csv

AAAAGATTTAGTTCTTTATG,46,,,,m64047_220402_055906.ccs.0--0-consensus.fasta
```

An open question is why there are more "lamassemble: using 1 out of x sequences" warnings and corresponding gaps in the Pacbio data than there are in the Nanopore data. The clusters that do produce consensus outputs also have overall lower proportions of sequences deemed similar enough to use. This is counter to what would be expected from the low Pacbio error rate.


## Sequence Confidence Bins

The Oxford Nanopore data for the blue libraries (Libraries 4 and 5) captured about 13000 more protein sequences than the PacBio data. However, the vast majority of these sequences were singletons, appearing in only one library with one barcode. Confidence level 4 had only 2,948 usable sequences.
The PacBio data had a higher proportion of sequences in the first four confidence categories and a lower proportion of singletons. 11,205 of the PacBio sequences fell into confidence level 4 and are usable.
Dr. Plesa's original analysis had 25,577 sequences with 16,367 of them falling into confidence level 4. Our results had a higher total number of sequences, but also a higher proportion of singletons. It is possible that we captured more gene-barcode pairs from the original data and picked up a bunch of extra singletons. However, our total amount of usable sequences in confidence level 4 or higher are much lower than that from the original analysis.


## Recommendations

Our pipeline was able to extract more gene-barcode pairs from the PacBio sequencing data than previous analyses. It was also able to extract data from the Oxford Nanopore sequencing results, making Oxford Nanopore a potentially viable option.

Based on the confidence bin results, PacBio data is still producing more gene-barcode pairs that could be usable for future experiments and/or training data. Oxford Nanopore either detects a high number of singletons, or accumulates enough errors that duplicate molecules appear to be singletons. **At this point we still have to recommend using PacBio sequencing for this application.**

However, the PacBio consensus sequences are based on much lower proportions of the gene sequences in each barcode cluster than the Oxford Nanopore consensus sequences. This may indicate more divergent sequences or more barcode collisions than expected in the PacBio data. The Oxford Nanopore consensus sequences are based on higher coverage as it stands, which may be good for reliability.

Further debugging of the lamassemble step may answer and solve the problem of why the Pacbio data is showing more gaps and lower sequence similarity. 

Alternately, fine-tuning starcode and lamassemble parameters may allow for improved clustering and consensus calling of Oxford Nanopore data.
