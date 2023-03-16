////////////////////////////// PARAMETERS //////////////////////////////

params.platform = "pacbio"
//params.platform = "nanopore"
params.infile = "/projects/bgmp/shared/groups/2022/SKU/plesa/test_files/pacbio/pacbio_q20_test.fastq"
// params.infile = "/projects/bgmp/shared/groups/2022/SKU/plesa/uploads/data/nanopore_raw/barcode0{1,2,3,4,5}d.fastq"
params.outdir = "$PWD/results/$workflow.start-results"
params.help = false
params.length = 1200

params.crfile = "$baseDir/sequences/conserved_regions.fasta"
params.indexfile = "$baseDir/sequences/library_indices.fasta"

STATS_SCRIPT = "$baseDir/src/summary_stats_hist.py"
DECONCAT_SCRIPT = "$baseDir/src/deconcatenation.py"
FILTERMAF_SCRIPT = "$baseDir/src/filterMaf.py"
EXTRACT_SCRIPT = "$baseDir/src/extractRegionsFasta_imperfect.py"
STARCODE_SCRIPT = "SOMETHING"
LAMASSEMBLE_SCRIPT = "$baseDir/src/runLamassemble.py"
FINALFORMAT_SCRIPT = "$baseDir/src/final_output_MSA.py"
CONFBINNNG_SCRIPT = "$baseDir/src/quality_binning.py"

//name_matcher = params.infile =~ /([^\/]+)\..+$/
//input_file = file(params.infile)
base_file_name = "test" //input_file.getSimpleName()
//println base_file_name


////////////////////////////// WORKFLOW //////////////////////////////

workflow {

    read_files_ch = Channel.fromPath(params.infile, checkIfExists: true).flatten()

    initial_stats(read_files_ch, "fastq")

    deconcat_ch = deconcat(read_files_ch, "fastq").deconcatfq.flatten()

    if (params.platform == 'pacbio')
        demuxed_ch = demux(deconcat_ch, "fastq").demuxfq.flatten()
    else if (params.platform == 'nanopore')
        demuxed_ch = deconcat_ch

    //prepro_ch = length_filter(demuxed_ch, "fasta").filteredfa.flatten()

    //last_ch = LAST(prepro_ch).filt-maf.flatten()

    //extract(prepro_ch, last_ch.filt-maf.flatten())

    //sc_cluster_ch = starcode_cluster()

    //lamassemble_cluster(prepro_ch, sc_cluster_ch) | final_format

    //conf_binning(lib4file, lib5file)

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

// step 5: Run LAST on preprocessed files, filter output
process LAST {

    publishDir path: "$params.outdir/05_LAST", mode: "copy", overwrite: false

    input:
    path infile

    output:
    path "*-raw.maf", emit: maf
    path "*-filt.maf", emit: filt-maf

    script:
    """
    if [[ ! -e "consdb.prj" ]]; then
        echo "Making LAST database"
        lastdb consdb $params.crfile
    else
        echo "LAST database or consdb.proj already exists."
    fi

    echo "Finding conserved regions in FASTA."
    lastal consdb $infile > $base_file_name-raw.maf

    $FILTERMAF_SCRIPT -i $base_file_name-raw.maf -o $base_file_name-filt.maf
    """
}

// step 6: Extract genes and barcodes
process extract {

    publishDir path: "$params.outdir/06_extract", mode: "copy", overwrite: false

    input:
    path infile_fasta
    path infile_maf

    output:
    path "$base_file_name*"

    script:
    """
    $EXTRACT_SCRIPT -f $infile_fasta -m $infile_maf -o $base_file_name
    """
}

// step 7: Cluster barcodes using Starcode
// process starcode_cluster {

//     publishDir path: "$params.outdir/07_starcode", mode: "copy", overwrite: false

//     input:
//     path infile

//     output:
//     path /// txt????

//     script:
//     """
//     starcode????
//     """
// }

//step 8: Cluster genes using lamassemble
process lamassemble_cluster {

    publishDir path: "$params.outdir/08_lamassemble", mode: "copy", overwrite: false

    input:
    path infile_fasta
    path infile_barcodes

    output:
    path "*consensus.fasta"

    script:
    """
    $LAMASSEMBLE_SCRIPT -f $infile_fasta -s $infile_barcodes -o $base_file_name-consensus.fasta -t $base_file_name\-temp
    """
}

//step 9: Format final output
process final_format {

    publishDir path: "$params.outdir/09_final_output", mode: "copy", overwrite: false

    input:
    path infile

    output:
    path "*.csv"

    script:
    """
    $FINALFORMAT_SCRIPT -f $infile -o $base_file_name-final.csv
    """
}

//step 10: Bin library 4 and 5 results into confidence categories
process conf_binning {

    publishDir path: "$params.outdir/10_confidence_bins", mode: "copy", overwrite: false

    input:
    path infile4
    path infile5

    output:
    path "*.csv"

    script:
    """
    $CONFBINNING_SCRIPT -lib4 abc -lib5 abc -o abc
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

