### First run of this pipeline: 

```
(M_Iso_Seq) [wesg@n0349 MAS-seq_Variants-UMIs]$ /usr/bin/time -v nextflow run main.nf --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/BLUE/PacBio_MAS_ISO_seq_GC3F_6762/m64047_230308_062131.ccs.bam --arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta -resume

 N E X T F L O W   ~  version 24.10.1

Launching `main.nf` [ecstatic_leibniz] DSL2 - revision: 785cb394a8

executor >  local (42)
[42/3a8602] process > initial_stats (1)       [100%] 1 of 1, cached: 1 ✔
[37/b9b26d] process > deconcat (1)            [100%] 1 of 1, cached: 1 ✔
[b5/81baa0] process > demux (1)               [100%] 1 of 1, cached: 1 ✔
[f5/e09da6] process > length_filter (9)       [100%] 9 of 9, cached: 9 ✔
[a8/31cb1b] process > LAST (4)                [100%] 9 of 9, cached: 2 ✔
[37/bbb3bc] process > extract (9)             [100%] 9 of 9, cached: 1 ✔
[9f/8a8697] process > starcode_cluster (9)    [100%] 9 of 9 ✔
[57/73ba6e] process > lamassemble_cluster (9) [100%] 9 of 9 ✔
[4d/2b87ec] process > final_format (9)        [100%] 9 of 9 ✔
Completed at: 23-Nov-2024 16:20:15
Duration    : 2d 5h 51m 51s
CPU hours   : 81.9 (2.3% cached)
Succeeded   : 42
Cached      : 15


        Command being timed: "nextflow run main.nf --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/BLUE/PacBio_MAS_ISO_seq_GC3F_6762/m64047_230308_062131.ccs.bam --arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta -resume"
        User time (seconds): 267996.43
        System time (seconds): 11450.68
        Percent of CPU this job got: 144%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 53:51:53
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 23036216
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 16518
        Minor (reclaiming a frame) page faults: 2660544288
        Voluntary context switches: 105293321
        Involuntary context switches: 2455672
        Swaps: 0
        File system inputs: 338720
        File system outputs: 364458072
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

