## 2024-11-24

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

# this command was manually terminated. At this point I really need to do some subsampling of the sequences going into lamassemble

(M_Iso_Seq) [wesg@n0351 MAS-seq_Variants-UMIs]$ /usr/bin/time -v nextflow run main.nf --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam --arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta

 N E X T F L O W   ~  version 24.10.1

Launching `main.nf` [distraught_shirley] DSL2 - revision: 785cb394a8

executor >  local (56)
[39/b65197] process > initial_stats (1)       [100%] 1 of 1 ✔
executor >  local (56)
[39/b65197] process > initial_stats (1)       [100%] 1 of 1 ✔
[d6/1b2655] process > deconcat (1)            [100%] 1 of 1 ✔
[0b/947a65] process > demux (1)               [100%] 1 of 1 ✔
[76/e692c8] process > length_filter (1)       [100%] 9 of 9 ✔
[86/50b91d] process > LAST (9)                [100%] 9 of 9 ✔
[83/a00109] process > extract (9)             [100%] 9 of 9 ✔
[1c/c078c0] process > starcode_cluster (9)    [100%] 9 of 9 ✔
[b5/faeb37] process > lamassemble_cluster (9) [ 88%] 8 of 9
[19/4db041] process > final_format (8)        [100%] 8 of 8

Command exited with non-zero status 1
        Command being timed: "nextflow run main.nf --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam --arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta"
        User time (seconds): 73260.10
        System time (seconds): 6868.86
        Percent of CPU this job got: 10%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 214:53:08
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 4288784
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 13524
        Minor (reclaiming a frame) page faults: 1484370648
        Voluntary context switches: 93609499
        Involuntary context switches: 2655996
        Swaps: 0
        File system inputs: 18008
        File system outputs: 59437504
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 1

```

At this point I added an if statement to the python script which does the calling of lamassemble. I am going to resume this run after switching branches. If this is working then I am going to merge the branch.

Here is the output. I am going to rerun both the datasets after I merge this sampling into the main branch.

```
(M_Iso_Seq) [wesg@n0351 MAS-seq_Variants-UMIs]$ /usr/bin/time -v nextflow run main.nf --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam --arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta -resume
Nextflow 24.10.2 is available - Please consider updating your version to it

 N E X T F L O W   ~  version 24.10.1

Launching `main.nf` [insane_dubinsky] DSL2 - revision: 785cb394a8

executor >  local (2)
[39/b65197] process > initial_stats (1)       [100%] 1 of 1, cached: 1 ✔
[d6/1b2655] process > deconcat (1)            [100%] 1 of 1, cached: 1 ✔
[0b/947a65] process > demux (1)               [100%] 1 of 1, cached: 1 ✔
[24/832016] process > length_filter (9)       [100%] 9 of 9, cached: 9 ✔
[e8/4d17ce] process > LAST (9)                [100%] 9 of 9, cached: 9 ✔
[b8/253105] process > extract (9)             [100%] 9 of 9, cached: 9 ✔
[a6/a36389] process > starcode_cluster (9)    [100%] 9 of 9, cached: 9 ✔
[0d/39d36d] process > lamassemble_cluster (7) [100%] 9 of 9, cached: 8 ✔
[f4/400a0b] process > final_format (9)        [100%] 9 of 9, cached: 8 ✔
Completed at: 01-Dec-2024 11:33:47
Duration    : 3h 58m 23s
CPU hours   : 26.6 (85% cached)
Succeeded   : 2
Cached      : 55


        Command being timed: "nextflow run main.nf --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam --arrfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/mas16_primers.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/MAS-seq_Variants-UMIs/sequences/barcodes.fasta -resume"
        User time (seconds): 12159.09
        System time (seconds): 3357.01
        Percent of CPU this job got: 108%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 3:58:25
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 39380660
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 2552
        Minor (reclaiming a frame) page faults: 615072878
        Voluntary context switches: 63049166
        Involuntary context switches: 123585
        Swaps: 0
        File system inputs: 3912
        File system outputs: 48518320
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```
