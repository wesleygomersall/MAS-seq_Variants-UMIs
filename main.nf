////////////////////////////// PARAMETERS //////////////////////////////

params.platform = "pacbio"
//params.platform = "nanopore"
params.infile = "/projects/bgmp/shared/groups/2022/SKU/plesa/test_files/pacbio/pacbio_q20_test.fastq"
// params.infile = "/projects/bgmp/shared/groups/2022/SKU/plesa/uploads/data/nanopore_raw/barcode0{1,2,3,4,5}d.fastq"
params.outdir = "$PWD/results/$workflow.start-results"
params.help = false
params.length = 1200

params.crfile = "./sequences/conserved_regions.fasta"
params.indexfile = "./sequences/library_indices.fasta"


STATS_SCRIPT = "./src/summary_stats_hist.py"
DECONCAT_SCRIPT = "./src/deconcatenation.py"

base_file_name = "test"

////////////////////////////// WORKFLOW //////////////////////////////

workflow {

    read_files_ch = Channel.fromPath(params.infile, checkIfExists: true).flatten()

    initial_stats(read_files_ch, "fastq")

    deconcat_ch = deconcat(read_files_ch, "fastq").deconcatfq.flatten()

    if (platform == 'pacbio')
        demuxed_ch = demux(deconcat_ch, "fastq").demuxfq.flatten()
    else if (platform == 'nanopore')
        demuxed_ch = deconcat_ch

    filtered_ch = length_filter(demuxed_ch, "fasta").filteredfa.flatten()
}

////////////////////////////// PROCESSES //////////////////////////////

if (params.help) {
	printHelp()
	exit 0
}

// step 1: get stats on input file
process initial_stats {

    publishDir path: "$params.outdir/01_initial-stats", mode: "copy", overwrite: false

    input:
    path infile
    val filetype

    output: // all outputs with base_file_name in the filename (captures png histogram and txt stats)
    path "$base_file_name*"

    script:
    """
    $STATS_SCRIPT -f $params.infile -o $base_file_name-initial-stats -t $filetype
    """
}

// step 2: deconcat input file
process deconcat {

    publishDir path: "$params.outdir/02_deconcat", mode: "copy", overwrite: false

    input:
    path infile
    val filetype
    
    output: // captures deconcat fastq (and deconcat/demux stats files for nanopore)
    path "$base_file_name-deconcat.fastq", emit: deconcatfq
    path "$base_file_name-stats.*", emit: deconcatstats, optional: true

    script:

    if (params.platform == 'pacbio')
        """
        $DECONCAT_SCRIPT -f $params.infile -o $base_file_name-deconcat.fastq -s $params.crfile
        """

    else if (params.platform == 'nanopore') // Nanopore is already demuxed, so run stats now on each FASTQ in folder
        """
        $DECONCAT_SCRIPT -f $params.infile -o $base_file_name-deconcat.fastq -s $params.crfile

        for f in ./*.fastq; do
            b=`basename \$f .fastq`
            $STATS_SCRIPT -f \$f -o \$b-stats -t $filetype
        done
        """
}

// step 3: demux deconcatenated file
process demux {

    publishDir path: "$params.outdir/03_demux", mode: "copy", overwrite: false

    input:
    path deconcat_files
    val filetype

    output: // captures demuxed fastqs and stats files for pacbio (and placeholder for nanopore)
    path "*demux*.fastq", emit: demuxfq, optional: true
    path "*demux*-stats.*", emit: demuxstats, optional: true

    script:
    if (params.platform == 'pacbio') // Pacbio is ready, run stats on each FASTQ in folder
        """
        lima --split $deconcat_files $params.indexfile $base_file_name-demux.fastq
        
        for f in ./*.fastq; do
            b=`basename \$f .fastq`
            $STATS_SCRIPT -f \$f -o \$b-stats -t $filetype
        done
        """

    else if (params.platform == 'nanopore')
        """
        echo "Already demultiplexed" > $base_file_name-already-demultiplexed.txt
        """
}

// step 4: length filter demuxed files
process length_filter {

    publishDir path: "$params.outdir/04_length-filter", mode: "copy", overwrite: false

    input:  // nanopore deconcat files, pacbio deconcat/demuxed files
    path infile
    val filetype

    output: // captures long and short filtered FASTAs
    path "*-filt.fasta", emit: filteredfa
    path "overlong/*.fasta", emit: overlongfa, optional: true
    path "*-stats.*", emit: filteredstats

    script: // splits each FASTQ into 2 FASTAs, below/above specified read length, then runs stats script again
    """
    n=`basename $infile .fastq`
    bioawk -c fastx '{
        if (length(\$seq) > $params.length) 
            print ">"\$name"\\n"\$seq > "/overlong/'\$n'.fasta"; 
        else 
            print ">"\$name"\\n"\$seq > "'\$n'-filt.fasta"
        }' $infile

    for f in ./*.fasta; do
        b=`basename \$f .fasta`
        $STATS_SCRIPT -f \$f -o \$b-stats -t $filetype
    done
    """
}


////////////////////////////// FUNCTIONS //////////////////////////////
def printHelp() 
{
    log.info"""\
            help
            """
            .stripIndent()
}