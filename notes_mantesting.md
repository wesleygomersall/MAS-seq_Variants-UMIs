## 2024-10-28

Manually running the pipeline from `BGMP_Plesa_project`.

In their nextflow file this is the process: 
1. inital_stats
	- Summary statistics on the input FASTQ data (we actually are supplied with SAM files) 
2. deconcat
	- Deconcatenates the masISO sequence array using the conserved sequences from the reads. We are not explicitly given this sequence, I have inferred it from the given sequence on benchling. 
	- This is an obsolete method and is replaced with `skera` from PacBio. 
3. demux 
	- Demultiplex the 9 bins of data. This uses `barcodes.fasta` to search for the sequences. 
	- PacBio `lima` gets this done.
4. length_filter
	- Filters reads out if they are too short (seq error)  or too long (didn't deconcat?) 
5. LAST
	- Run LAST alignment for creating maf file. I think there is also a section here where they get statistics about that maf file. 
6. extract
	- Extract the sequences from trimmed FASTQ files: Using conserved sequences it identifies protein variant sequences and the UMI sequences. 
	- Removes the conserved regions from the read. Cuts the UMI and sticks it at the beginning of the read.
	- Create 3 fasta files: one with just barcodes, one with just sequences (these two will be used later), and one with barcode immediately followed by Sequence. 
7. starcode_cluster
	- Run starcode on the barcode+sequence.fasta file from the previous step. 
	- returns the consensus sequences, but these have no associated barcodes with them, so this output needs to be compared back to the barcode and sequence fasta files from the last step separately. 
8. lamassemble_cluster
	- What does this do ?
9. final_format
	- Creates final CSV with all the data collected in the last couple steps. 
	- This also transcribes the DNA into protein sequence and returns both the full protein sequence and the protein sequence only up to the first STOP codon (the functional protein)


The files from lima output:

`/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/blue_pb/m64047_230308_062131.ccs.demux.bam`
`/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/red_pb/m64047_230306_210601.ccs.demux.bam` 

The barcode sequence fasta:
`/projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta`

After they ran lima they did length filtering with the script: 
`/projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/src/script.py`

## 2024-11-17

Here I am going to start from the beginning and deconcatenate the data with both their script and with the program `skera`. First I am going to compare their outputs and then see if it is as easy as doing a 1:1 swap in the NextFlow.  

The script I am going to run in the pbTools env is `deconcatenation.py` in their `src` folder. The following is the argparse help:

```
(pbTools) [wesg@n0349 src]$ ./deconcatenation.py --help
usage: deconcatenation.py [-h] -f FILE -o OUTPUT -s SEQUENCES

Get file paths for input FASTQ file and output monomer FASTQ file.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Absolute path to input file
  -o OUTPUT, --output OUTPUT
                        Output monomer filename
  -s SEQUENCES, --sequences SEQUENCES
                        FASTA filename containing sequences of 3 conserved regions
```

The command I am going to execute is this:

```
./src/deconcatenation.py -f ./sequences/bluereads.fastq -o /projects/bgmp/shared/groups/2024/novel-fluor/wesg/manualtesting/pyoutput.fastq -s ./sequences/conserved_regions.fasta
```

Compare this to the file `/gpfs/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/NF_pacbio_output/blu/02_deconcat/bluereads-deconcat.fastq`. These should be the same. I can keep the output directory consistent if I can run `lima` on the output of `skera` and modify the command to just output fastq files from `lima`. I will run `skera` on the raw SAM files and then use `samtools` to compare the results. There should be a similar number of reads, but hopefully more using `skera`. Then will do `fastqc` to compare these files.

I think the final goal is to remove the first step in NextFlow, becuase it isn't going to be compatible with the SAM data. Go staight into `skera` + `lima` and then add the R scripts for `lima` statistics.

The command(s) to get that `skera` comparison:
```
# in the pbLimaSkera env:
source activate /projects/bgmp/shared/groups/2024/novel-fluor/envs/pbLimaSkera/
/usr/bin/time -v skera split /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/BLUE/PacBio_MAS_ISO_seq_GC3F_6762/m64047_230308_062131.ccs.bam \
					/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/mas16_primers.fasta \
					/projects/bgmp/shared/groups/2024/novel-fluor/wesg/manualtesting/skeraoutput.bam
conda deactivate
# use samtools and fastqc to compare these two outputs
conda activate Stacks
samtools fastq /projects/bgmp/shared/groups/2024/novel-fluor/wesg/manualtesting/skeraoutput.bam > /projects/bgmp/shared/groups/2024/novel-fluor/wesg/manualtesting/skeraoutput.fastq
conda deactivate
```

Immediate notes: 
- `skera` was substantially faster
- `skera` had almost 3x as many reads as `deconcatenate.py` 
- FastQC outputs were quite similar. 

## 2024-11-18

Look at the ouput of `skera` and put it through `lima`. Last time I ran this it seemed that it produced a single output bam file. I need to figure out how to output to distinct files for the 9 bins, and ideally directly to fastq format. Try the options `--same` and `--split` which were used in the original `lima` command in NextFlow.

Here is the command that should do it: 

```
# the command in the nextflow: lima --same --split $infile $params.indexfile $base_file_name\\.fastq
/usr/bin/time -v lima --same --split skeraoutput.bam ../BGMP_Plesa_project/sequences/barcodes.fasta sk_lima_output.fastq
```
