# Novel fluorescent proteins!

## 2024-10-22

It is Mia's 18th birthday today! 

I need to make a conda environment to process the PacBio reads using PacBio's software lima and skera. See: 
- https://github.com/PacificBiosciences/pbbioconda?tab=readme-ov-file 
- https://github.com/pacificbiosciences/barcoding/
- https://github.com/pacificbiosciences/skera/

```
cd /gpfs/projects/bgmp/shared/groups/2024/novel-fluor/envs

conda create --prefix=pbLimaSkera python=3.12
source activate pbLimaSkera
conda install -c bioconda lima
conda install -c bioconda pbskera
```

This conda environment is in `/gpfs/projects/bgmp/shared/groups/2024/novel-fluor/envs`.
To activate it go to the directory above and run `source activate ./yourEnvName`.

### skera
```
skera - PacBio Concatenated Read Splitter

Usage:
  skera <tool>

  -h,--help    Show this help and exit.
  --version    Show application version and exit.

Tools:
  split      splits sequences at adapter locations
  undo       undo skera split

Copyright (C) 2004-2023     Pacific Biosciences of California, Inc.
This program comes with ABSOLUTELY NO WARRANTY; it is intended for
Research Use Only and not for use in diagnostic procedures.

```

### lima 

```
lima - Lima, Demultiplex Barcoded PacBio Data and Clip Barcodes

Usage:
  lima [options] <INPUT.bam|xml|fa|fq|gz> <BARCODES.fa> <OUTPUT.bam|xml|fa|fq|gz>

  INPUT.bam|xml|fa|fq|gz         STR    Subread or CCS BAM, SubreadSet or ConsensusReadSet XML, CCS FASTA/FASTQ [.gz]
  BARCODES.fa                    STR    Barcode FASTA or BarcodeSet XML
  OUTPUT.bam|xml|fa|fq|gz        STR    Subread or CCS BAM, SubreadSet or ConsensusReadSet XML, CCS FASTA/FASTQ [.gz]

Library Design:
  -s,--same                             Only keep same barcodes in a pair in output.
  -d,--different                        Only keep different barcodes in a pair in output. Enforces --min-passes ≥ 1.
  -N,--neighbors                        Only output barcode pairs that are neighbors in barcode file.
  --hifi-preset                  STR    Recommended settings. See below for preset parameter details. [NONE]
  --omit-barcode-infix                  Omit barcode infix in file names.

Input Limitations:
  -p,--per-read                         Do not tag per ZMW, but per read.
  -f,--score-full-pass                  Only use subreads flanked by adapters for barcode identification.
  -n,--max-scored-barcode-pairs  INT    Only use up to N barcode pair regions to find the barcode, 0 means use all. [0]
  -b,--max-scored-barcodes       INT    Analyze at maximum the provided number of barcodes per ZMW; 0 means
                                        deactivated. [0]
  -a,--max-scored-adapters       INT    Analyze at maximum the provided number of adapters per ZMW; 0 means
                                        deactivated. [0]
  -u,--min-passes                INT    Minimal number of full passes. [0]
  -l,--min-length                INT    Minimum sequence length after clipping. [50]
  -L,--max-input-length          INT    Maximum input sequence length, 0 means deactivated. [0]
  -M,--bad-adapter-ratio         FLOAT  Maximum ratio of bad adapter. [0]
  -P,--shared-prefix                    Barcodes may be substrings of others.

Barcode Region:
  -w,--window-size-multi         FLOAT  The candidate region size multiplier: barcode_length * multiplier. [3]
  -W,--window-size               INT    The candidate region size in bp. If set, --window-size-mult will be ignored.
                                        [0]
  -r,--min-ref-span              FLOAT  Minimum reference span relative to the barcode length. [0.5]
  -R,--min-scoring-regions       INT    Minimum number of barcode regions with sufficient relative span to the barcode
                                        length. [1]

Score Filters:
  -m,--min-score                 INT    Reads below the minimum barcode score are removed from downstream analysis. [0]
  -i,--min-end-score             INT    Minimum end barcode score threshold is applied to the individual leading and
                                        trailing ends. [0]
  -x,--min-signal-increase       INT    The minimal score difference, between first and combined, required to call a
                                        barcode pair different. [10]
  -y,--min-score-lead            INT    The minimal score lead required to call a barcode pair significant. [10]

Index Sorting:
  -k,--keep-tag-idx-order               Keep identified order of barcode pair indices in BC tag; CCS only.
  -K,--keep-split-idx-order             Keep identified order of barcode pair indices in split output names; CCS only.

Aligner Configuration:
  --ccs                                 CCS mode, use optimal alignment options -A 1 -B 4 -D 3 -I 3 -X 4.
  -A,--match-score               INT    Score for a sequence match. [4]
  -B,--mismatch-penalty          INT    Penalty for a mismatch. [13]
  -D,--deletion-penalty          INT    Deletions penalty. [7]
  -I,--insertion-penalty         INT    Insertion penalty. [7]
  -X,--branch-penalty            INT    Branch penalty. [4]

Output Splitting:
  --split                               Split output by barcode pair.
  --split-named                         Split output by resolved barcode pair name.
  -F,--files-per-directory       INT    Group maximum numbers of split barcode output files per directory; 0 means
                                        deactivated. [0]
  --split-subdirs                       Output each barcode into its own sub-directory, only works with output
                                        splitting.
  -U,--reuse-biosample-uuids            Use UUIDs from BioSamples, must be used with output BAM splitting.
  --reuse-source-uuid                   Use UUID from input dataset XML.
  --no-clip                             Call barcodes, but do not clip them from read sequences.

Output Restrictions:
  --output-handles               INT    Maximum number of open output files. [500]
  --dump-clips                          Dump clipped regions in a separate output file <prefix>.lima.clips
  --store-unbarcoded                    Store unbarcoded reads to <prefix>.removed.SUFFIX
  --no-output                           Do not generate demultiplexed output.
  --no-reports                          Do not generate reports.
  --output-missing-pairs                Output all barcode pairs from biosamples, irrespective of presence.

Single Side:
  -S,--single-side                      Assign single side barcodes by score clustering.
  --scored-adapter-ratio         FLOAT  Minimum ratio of scored vs sequenced adapters. [0.25]
  --ignore-missing-adapters             Ignore flanks of consensus reads labeled as missing adapter.

IsoSeq:
  --isoseq                              Activate specialized IsoSeq mode.

Advanced:
  --peek                         INT    Demux the first N ZMWs and return the mean score; 0 means peeking deactivated.
                                        [0]
  --guess                        INT    Try to guess the used barcodes, using the provided mean score threshold; 0
                                        means guessing deactivated. [0]
  --guess-min-count              INT    Minimum number of ZMWs observed to whitelist barcodes. [0]
  --peek-guess                          Try to infer the used barcodes subset.
  --ignore-xml-biosamples               Ignore <BioSamples> from XML input.
  --biosample-csv                STR    CSV file, barcode pairs with associated biosample names.
  --overwrite-biosample-names           In isoseq mode, overwrite existing sample names in the SM tag

  -h,--help                             Show this help and exit.
  --version                             Show application version and exit.
  -j,--num-threads               INT    Number of threads to use, 0 means autodetection. [0]
  --log-level                    STR    Set log level. Valid choices: (TRACE, DEBUG, INFO, WARN, FATAL). [WARN]
  --log-file                     FILE   Log to a file, instead of stderr.

Using --peek-guess is equivalent to:
  --peek 50000 --guess 45 --guess-min-count 10.
If used in combination with --isoseq:
  --peek 50000 --guess 75 --guess-min-count 100.
If used in combination with --ccs:
  --peek 50000 --guess 75 --guess-min-count 10.

Recommended parameter combinations of --hifi-preset:
  SYMMETRIC          : --ccs --min-score 0 --min-end-score 80 --min-ref-span 0.75 --same --single-end
  SYMMETRIC-ADAPTERS : --ccs --min-score 0 --min-end-score 80 --min-ref-span 0.75 --same --ignore-missing-adapters --single-end
  ASYMMETRIC         : --ccs --min-score 80 --min-end-score 50 --min-ref-span 0.75 --different --min-scoring-regions 2

Copyright (C) 2004-2023     Pacific Biosciences of California, Inc.
This program comes with ABSOLUTELY NO WARRANTY; it is intended for
Research Use Only and not for use in diagnostic procedures.
```



So the PacBio files I ned to deal with are these: 
- `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/BLUE/PacBio_MAS_ISO_seq_GC3F_6762/m64047_230308_062131.ccs.bam`
- `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/BLUE/PacBio_MAS_ISO_seq_GC3F_6762/m64047_230308_062131.ccs.bam.pbi`
- `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam`
- `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam.pbi`

These are the barcode files: 
- `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/mas16_primers.fasta`
- `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/barcodes.fasta`

### First to use skera: 

First I make an output directory for the output of all this data: `/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat`
  
From the documentation at https://skera.how/

	Skera split run on HiFi reads in PacBio BAM format:

	`skera split <movie>.hifi_reads.bam adapters.fasta <movie>.skera.bam`

Here is the exact command I am using for the first file: 

```

skera split /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/BLUE/PacBio_MAS_ISO_seq_GC3F_6762/m64047_230308_062131.ccs.bam \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/mas16_primers.fasta \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/blue_pb/m64047_230308_062131.ccs.skera.bam

```

And for the second file: 

```
skera split /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/mas16_primers.fasta \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/red_pb/m64047_230306_210601.ccs.skera.bam
```

If this works then the next step is to run the lima on this data from skera: 

From the documentation at https://lima.how/

Question: Are these barcodes asymmetric or symetric for this step? 
I think that they are symmetrically barcoded

```
# First sample (blue) 
lima /projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/blue_pb/m64047_230308_062131.ccs.skera.bam \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/barcodes.fasta \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/blue_pb/m64047_230308_062131.ccs.demux.bam \
	--hifi-preset SYMMETRIC


# Second sample (red) 
lima /projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/red_pb/m64047_230306_210601.ccs.skera.bam \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/barcodes.fasta \
	/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/red_pb/m64047_230306_210601.ccs.demux.bam \
	--hifi-preset SYMMETRIC
```

The final files are named `<file>.demux.bam`

## 2024-10-24 

Running QC for this data. Mahmoud is currently creating environment for and installing Starcode program for determining consensus variants per barcode.

See https://lima.how/faq/qc.html

Copy these scripts to Talapas at `/projects/bgmp/shared/groups/2024/novel-fluor/wesg/lima_r`

I will add R to a new conda environment named R and install the following dependencies for this code: 

```
cd /gpfs/projects/bgmp/shared/groups/2024/novel-fluor/envs

conda create --prefix=R
source activate R
conda install -y -c r-base # just to get R
conda install -y r-ggplot2 r-tidyr r-dplyr r-viridis r-scales r-data.table # packages in R

```
Activate the environment with `conda activate /gpfs/projects/bgmp/shared/groups/2024/novel-fluor/envs/R`
or navigate to `/gpfs/projects/bgmp/shared/groups/2024/novel-fluor/envs` and run `source activate ./R`

Run the followingg command: 

```
/usr/bin/time -v Rscript --vanilla report_detail.R ../dat/blue_pb/m64047_230308_062131.ccs.demux.lima.report
```
This ran out of memory with 16G. I am going to give it 64G and run again. 

## 2024-10-27

This is the env needed to run the 2022-2023 group's work.

```
conda create --prefix=pbTools
conda install -y python=3.10
conda install -y bioconda::nextflow
conda install -y bioawk=1.0
conda install -y matplotlib=3.7.1
conda install -y biopython=1.81
conda install -y bioconda::last

conda install -y regex=2022-10-31
conda install -y bioconda::lima
conda install -y java=11 # did this work?
conda install -y starcode=1.4
conda install -y lamassemble # not specified any version in the dependencies
```
This should be it: 

<details>
<summary> The env `pbTools` </summary>

```
# packages in environment at /gpfs/projects/bgmp/shared/groups/2024/novel-fluor/envs/pbTools:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-forge
_openmp_mutex             4.5                       2_gnu    conda-forge
alsa-lib                  1.2.12               h4ab18f5_0    conda-forge
attr                      2.5.1                h166bdaf_1    conda-forge
bioawk                    1.0                 he4a0461_12    bioconda
biopython                 1.81            py310h2372a71_1    conda-forge
brotli                    1.1.0                hb9d3cd8_2    conda-forge
brotli-bin                1.1.0                hb9d3cd8_2    conda-forge
bzip2                     1.0.8                h4bc722e_7    conda-forge
c-ares                    1.34.2               heb4867d_0    conda-forge
ca-certificates           2024.8.30            hbcca054_0    conda-forge
cairo                     1.18.0               hbb29018_2    conda-forge
certifi                   2024.8.30          pyhd8ed1ab_0    conda-forge
contourpy                 1.3.0           py310h3788b33_2    conda-forge
coreutils                 9.5                  hd590300_0    conda-forge
curl                      8.10.1               hbbe4b11_0    conda-forge
cycler                    0.12.1             pyhd8ed1ab_0    conda-forge
dbus                      1.13.6               h5008d03_3    conda-forge
expat                     2.6.3                h5888daf_0    conda-forge
font-ttf-dejavu-sans-mono 2.37                 hab24e00_0    conda-forge
font-ttf-inconsolata      3.000                h77eed37_0    conda-forge
font-ttf-source-code-pro  2.038                h77eed37_0    conda-forge
font-ttf-ubuntu           0.83                 h77eed37_3    conda-forge
fontconfig                2.14.2               h14ed4e7_0    conda-forge
fonts-conda-ecosystem     1                             0    conda-forge
fonts-conda-forge         1                             0    conda-forge
fonttools                 4.54.1          py310h89163eb_1    conda-forge
freetype                  2.12.1               h267a509_2    conda-forge
gawk                      5.3.1                hcd3d067_0    conda-forge
gettext                   0.22.5               he02047a_3    conda-forge
gettext-tools             0.22.5               he02047a_3    conda-forge
giflib                    5.2.2                hd590300_0    conda-forge
glib                      2.82.2               h44428e9_0    conda-forge
glib-tools                2.82.2               h4833e2c_0    conda-forge
gmp                       6.3.0                hac33072_2    conda-forge
graphite2                 1.3.13            h59595ed_1003    conda-forge
gst-plugins-base          1.24.7               h0a52356_0    conda-forge
gstreamer                 1.24.7               hf3bb09a_0    conda-forge
harfbuzz                  8.5.0                hfac3d4d_0    conda-forge
icu                       73.2                 h59595ed_0    conda-forge
keyutils                  1.6.1                h166bdaf_0    conda-forge
kiwisolver                1.4.7           py310h3788b33_0    conda-forge
krb5                      1.21.3               h659f571_0    conda-forge
lamassemble               1.7.2              pyh7cba7a3_0    bioconda
lame                      3.100             h166bdaf_1003    conda-forge
last                      1595                 h43eeafb_0    bioconda
lcms2                     2.16                 hb7c19ff_0    conda-forge
ld_impl_linux-64          2.43                 h712a8e2_2    conda-forge
lerc                      4.0.0                h27087fc_0    conda-forge
libasprintf               0.22.5               he8f35ee_3    conda-forge
libasprintf-devel         0.22.5               he8f35ee_3    conda-forge
libblas                   3.9.0           25_linux64_openblas    conda-forge
libbrotlicommon           1.1.0                hb9d3cd8_2    conda-forge
libbrotlidec              1.1.0                hb9d3cd8_2    conda-forge
libbrotlienc              1.1.0                hb9d3cd8_2    conda-forge
libcap                    2.69                 h0f662aa_0    conda-forge
libcblas                  3.9.0           25_linux64_openblas    conda-forge
libclang-cpp15            15.0.7          default_h127d8a8_5    conda-forge
libclang13                19.1.2          default_h9c6a7e4_1    conda-forge
libcups                   2.3.3                h4637d8d_4    conda-forge
libcurl                   8.10.1               hbbe4b11_0    conda-forge
libdeflate                1.22                 hb9d3cd8_0    conda-forge
libedit                   3.1.20191231         he28a2e2_2    conda-forge
libev                     4.33                 hd590300_2    conda-forge
libevent                  2.1.12               hf998b51_1    conda-forge
libexpat                  2.6.3                h5888daf_0    conda-forge
libffi                    3.4.2                h7f98852_5    conda-forge
libflac                   1.4.3                h59595ed_0    conda-forge
libgcc                    14.2.0               h77fa898_1    conda-forge
libgcc-ng                 14.2.0               h69a702a_1    conda-forge
libgcrypt                 1.11.0               h4ab18f5_1    conda-forge
libgettextpo              0.22.5               he02047a_3    conda-forge
libgettextpo-devel        0.22.5               he02047a_3    conda-forge
libgfortran               14.2.0               h69a702a_1    conda-forge
libgfortran-ng            14.2.0               h69a702a_1    conda-forge
libgfortran5              14.2.0               hd5240d6_1    conda-forge
libglib                   2.82.2               h2ff4ddf_0    conda-forge
libgomp                   14.2.0               h77fa898_1    conda-forge
libgpg-error              1.50                 h4f305b6_0    conda-forge
libiconv                  1.17                 hd590300_2    conda-forge
libjpeg-turbo             3.0.0                hd590300_1    conda-forge
liblapack                 3.9.0           25_linux64_openblas    conda-forge
libllvm15                 15.0.7               hb3ce162_4    conda-forge
libllvm19                 19.1.2               ha7bfdaf_0    conda-forge
libnghttp2                1.64.0               h161d5f1_0    conda-forge
libnsl                    2.0.1                hd590300_0    conda-forge
libogg                    1.3.5                h4ab18f5_0    conda-forge
libopenblas               0.3.28          pthreads_h94d23a6_0    conda-forge
libopus                   1.3.1                h7f98852_1    conda-forge
libpng                    1.6.44               hadc24fc_0    conda-forge
libpq                     16.4                 h2d7952a_3    conda-forge
libsndfile                1.2.2                hc60ed4a_1    conda-forge
libsqlite                 3.47.0               hadc24fc_0    conda-forge
libssh2                   1.11.0               h0841786_0    conda-forge
libstdcxx                 14.2.0               hc0a3c3a_1    conda-forge
libstdcxx-ng              14.2.0               h4852527_1    conda-forge
libsystemd0               256.7                h2774228_1    conda-forge
libtiff                   4.7.0                he137b08_1    conda-forge
libuuid                   2.38.1               h0b41bf4_0    conda-forge
libvorbis                 1.3.7                h9c3ff4c_0    conda-forge
libwebp-base              1.4.0                hd590300_0    conda-forge
libxcb                    1.17.0               h8a09558_0    conda-forge
libxcrypt                 4.4.36               hd590300_1    conda-forge
libxkbcommon              1.7.0                h2c5496b_1    conda-forge
libxml2                   2.12.7               h4c95cb1_3    conda-forge
libzlib                   1.3.1                hb9d3cd8_2    conda-forge
lima                      2.9.0                h9ee0642_1    bioconda
lz4-c                     1.9.4                hcb278e6_0    conda-forge
mafft                     7.526                h4bc722e_0    conda-forge
matplotlib                3.7.1           py310hff52083_0    conda-forge
matplotlib-base           3.7.1           py310he60537e_0    conda-forge
mpfr                      4.2.1                h90cbb55_3    conda-forge
mpg123                    1.32.8               hc50e24c_0    conda-forge
munkres                   1.1.4              pyh9f0ad1d_0    conda-forge
mysql-common              8.3.0                h70512c7_5    conda-forge
mysql-libs                8.3.0                ha479ceb_5    conda-forge
ncurses                   6.5                  he02047a_1    conda-forge
nextflow                  24.04.4              hdfd78af_0    bioconda
nspr                      4.36                 h5888daf_0    conda-forge
nss                       3.106                hdf54f9c_0    conda-forge
numpy                     1.26.4          py310hb13e2d6_0    conda-forge
openjdk                   21.0.0               haa376d0_0    conda-forge
openjpeg                  2.5.2                h488ebb8_0    conda-forge
openssl                   3.3.2                hb9d3cd8_0    conda-forge
packaging                 24.1               pyhd8ed1ab_0    conda-forge
parallel                  20240922             ha770c72_0    conda-forge
pcre2                     10.44                hba22ea6_2    conda-forge
perl                      5.32.1          7_hd590300_perl5    conda-forge
pillow                    11.0.0          py310hfeaa1f3_0    conda-forge
pip                       24.2               pyh8b19718_1    conda-forge
pixman                    0.43.2               h59595ed_0    conda-forge
ply                       3.11               pyhd8ed1ab_2    conda-forge
pthread-stubs             0.4               hb9d3cd8_1002    conda-forge
pulseaudio-client         17.0                 hb77b528_0    conda-forge
pyparsing                 3.2.0              pyhd8ed1ab_1    conda-forge
pyqt                      5.15.9          py310h04931ad_5    conda-forge
pyqt5-sip                 12.12.2         py310hc6cd4ac_5    conda-forge
python                    3.10.15         h4a871b0_2_cpython    conda-forge
python-dateutil           2.9.0              pyhd8ed1ab_0    conda-forge
python_abi                3.10                    5_cp310    conda-forge
qt-main                   5.15.8              ha2b5568_22    conda-forge
readline                  8.2                  h8228510_1    conda-forge
regex                     2022.10.31      py310h5764c6d_0    conda-forge
setuptools                75.1.0             pyhd8ed1ab_0    conda-forge
sip                       6.7.12          py310hc6cd4ac_0    conda-forge
six                       1.16.0             pyh6c4a22f_0    conda-forge
starcode                  1.4                  h031d066_5    bioconda
tk                        8.6.13          noxft_h4845f30_101    conda-forge
toml                      0.10.2             pyhd8ed1ab_0    conda-forge
tomli                     2.0.2              pyhd8ed1ab_0    conda-forge
tornado                   6.4.1           py310ha75aee5_1    conda-forge
tzdata                    2024b                hc8b5060_0    conda-forge
unicodedata2              15.1.0          py310ha75aee5_1    conda-forge
wheel                     0.44.0             pyhd8ed1ab_0    conda-forge
xcb-util                  0.4.1                hb711507_2    conda-forge
xcb-util-image            0.4.0                hb711507_2    conda-forge
xcb-util-keysyms          0.4.1                hb711507_0    conda-forge
xcb-util-renderutil       0.3.10               hb711507_0    conda-forge
xcb-util-wm               0.4.2                hb711507_0    conda-forge
xkeyboard-config          2.43                 hb9d3cd8_0    conda-forge
xorg-libice               1.1.1                hb9d3cd8_1    conda-forge
xorg-libsm                1.2.4                he73a12e_1    conda-forge
xorg-libx11               1.8.10               h4f16b4b_0    conda-forge
xorg-libxau               1.0.11               hb9d3cd8_1    conda-forge
xorg-libxdmcp             1.1.5                hb9d3cd8_0    conda-forge
xorg-libxext              1.3.6                hb9d3cd8_0    conda-forge
xorg-libxfixes            6.0.1                hb9d3cd8_0    conda-forge
xorg-libxi                1.8.2                hb9d3cd8_0    conda-forge
xorg-libxrender           0.9.11               hb9d3cd8_1    conda-forge
xorg-libxt                1.3.0                hb9d3cd8_2    conda-forge
xorg-libxtst              1.2.5                hb9d3cd8_3    conda-forge
xorg-libxxf86vm           1.1.5                hb9d3cd8_4    conda-forge
xorg-xf86vidmodeproto     2.3.1             hb9d3cd8_1004    conda-forge
xorg-xorgproto            2024.1               hb9d3cd8_1    conda-forge
xz                        5.2.6                h166bdaf_0    conda-forge
zlib                      1.3.1                hb9d3cd8_2    conda-forge
zstd                      1.5.6                ha6fb4c9_0    conda-forge
(pbTools) [wesg@login1 envs]$
```
</details>

I need the fasta sequences of the 9 bins. `/projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/barcodes.fasta`

The last thing(s) I need to collect are the conserved region sequences in a fasta file output. The first place I can look is on the sample sequence provided by Calin on the initial project description page.  

Best guess at the fasta for this one:

### Conserved region sequences (from benchling sequence)

```
>CR1
CTACACGACGCTCTTCCGATCTCACATATCAGAGTGCGTGTGAGCGGATAACAATTTCACACAGGAAACAGCTCATATG
>CR2
CtaaGTGTGGCTGCGGAAC
>CR3
AAGCAGTGGTATCAACGCAGAGCGCACTCTGATATGTGCGAAAAGTGCCACCTGACGTCGTGC
```

The PacBio FASTQ files (created from raw data with `samtools fastq`) are here: 
- `/projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/bluereads.fastq`
- `/projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/redreads.fastq`

These are the barcode/conserved region files (At least the conserved region file MUST be here, there is a reference to this path in the nextflow script): 
- `/projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta`
- `/projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta`

## 2024-10-28

On the github README, they say that the location of starcode needs to be updated. First I would like to just see this pipeline working through the various scripts before I worry too much about this last step. 

To run this old pipeline I will do the following: 

```
cd /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project

# blue reads
/usr/bin/time -v nextflow ./main.nf --infile sequences/bluereads.fastq --outdir /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs/blu --crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta 

# red reads
/usr/bin/time -v nextflow ./main.nf --infile sequences/redreads.fastq --outdir /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs/red --crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta 
```

## 2024-10-29

The git repo for this pipeline mentions that the location for starcode must be updated before running the script. This is why nextflow breaks at this step. The file is trying to use a local install that doesn't exist, or if it does, exists in a directory off-limits to myself. 

I have installed starcode 1.4 with bioconda so I am just going to forget about pointing to the local install and call it without the absolute path. Instead I swapped the to using the command `starcode`. At this point the thing should run all the way through.

## 2024-10-30

These ran successfully. See the outputs below. The output data will be copied to `/projects/bgmp/shared/groups/2024/novel-fluor/shared/dat/NF_pacbio_output`

### blue

```
(pbTools) [wesg@n0349 BGMP_Plesa_project]$ /usr/bin/time -v nextflow ./main.nf --infile sequences/bluereads.fastq --outdir /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs/blu --crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta

 N E X T F L O W   ~  version 24.04.4

Launching `./main.nf` [determined_lalande] DSL2 - revision: 184a2e8f89

executor >  local (57)
[cb/f73cf9] initial_stats (1)       | 1 of 1 ✔
[41/379806] deconcat (1)            | 1 of 1 ✔
[d5/5abe42] demux (1)               | 1 of 1 ✔
[d6/70750c] length_filter (1)       | 9 of 9 ✔
[48/605c17] LAST (9)                | 9 of 9 ✔
[07/bd3ba6] extract (9)             | 9 of 9 ✔
[3d/5ae593] starcode_cluster (9)    | 9 of 9 ✔
[b9/d08fb1] lamassemble_cluster (9) | 9 of 9 ✔
[44/785a60] final_format (9)        | 9 of 9 ✔
Completed at: 30-Oct-2024 20:33:25
Duration    : 1d 2h 11m 46s
CPU hours   : 41.8
Succeeded   : 57


        Command being timed: "nextflow ./main.nf --infile sequences/bluereads.fastq --outdir /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs/blu --crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta"
        User time (seconds): 117006.99
        System time (seconds): 20263.16
        Percent of CPU this job got: 145%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 26:11:48
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 10500460
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 85314
        Minor (reclaiming a frame) page faults: 3258972254
        Voluntary context switches: 128781846
        Involuntary context switches: 3033437
        Swaps: 0
        File system inputs: 2008
        File system outputs: 102009032
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0


```

### red

```
(pbTools) [wesg@n0350 BGMP_Plesa_project]$ /usr/bin/time -v nextflow ./main.nf --infile sequences/redreads.fastq --outdir /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs/red --crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta

 N E X T F L O W   ~  version 24.04.4

Launching `./main.nf` [wise_yonath] DSL2 - revision: 184a2e8f89

executor >  local (57)
[19/59955d] initial_stats (1)     | 1 of 1 ✔
[64/1b2b61] deconcat (1)          | 1 of 1 ✔
[81/47c7e5] demux (1)             | 1 of 1 ✔
[9d/52a96b] length_filter (1)     | 9 of 9 ✔
[1d/04ca68] LAST (9)              | 9 of 9 ✔
[0d/0cd699] extract (9)           | 9 of 9 ✔
[c0/1fd03b] starcode_cluster (9)  | 9 of 9 ✔
[52/81150d] lam…emble_cluster (9) | 9 of 9 ✔
[a3/a83bfc] final_format (9)      | 9 of 9 ✔
Completed at: 03-Nov-2024 05:12:03
Duration    : 4d 11h 50m 19s
CPU hours   : 116.7
Succeeded   : 57


        Command being timed: "nextflow ./main.nf --infile sequences/redreads.fastq --outdir /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs/red --crfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/conserved_regions.fasta --indexfile /projects/bgmp/shared/groups/2024/novel-fluor/wesg/BGMP_Plesa_project/sequences/barcodes.fasta"
        User time (seconds): 397080.79
        System time (seconds): 13993.56
        Percent of CPU this job got: 105%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 107:50:21
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 27017448
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 28929
        Minor (reclaiming a frame) page faults: 4160226933
        Voluntary context switches: 131568592
        Involuntary context switches: 2301069
        Swaps: 0
        File system inputs: 184
        File system outputs: 205037136
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0

```

After this I moved the data to the shared folder.

```
cd /projects/bgmp/shared/groups/2024/novel-fluor/wesg/outputs
mv -r * ../../shared/dat/NF_pacbio_output/
```
