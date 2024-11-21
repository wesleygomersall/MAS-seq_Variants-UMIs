////////////////////////////// PARAMETERS //////////////////////////////

params.platform = "pacbio"
params.infile = "input file path goes here"
params.outdir = "$PWD/results/$workflow.start-results"
params.help = false
params.length = 1200

// params.crfile = "$baseDir/sequences/conserved_regions.fasta"
params.arrfile = "$baseDir/sequences/mas16_primers.fasta"
params.indexfile = "$baseDir/sequences/barcodes.fasta"

// STATS_SCRIPT = "$baseDir/src/summary_stats_hist.py"
// DECONCAT_SCRIPT = "$baseDir/src/deconcatenation.py"
FILTERMAF_SCRIPT = "$baseDir/src/filterMaf.py"
SUMMAF_SCRIPT = "$baseDir/src/summarize_maf.py"
EXTRACT_SCRIPT = "$baseDir/src/extractRegionsFasta_withEnds.py"
// STARCODE_LOCATION = "/projects/bgmp/shared/groups/2022/SKU/plesa/starcode/starcode"
LAMASSEMBLE_SCRIPT = "$baseDir/src/runLamassemble.py"
FINALFORMAT_SCRIPT = "$baseDir/src/final_output_MSA.py"

////////////////////////////// WORKFLOW //////////////////////////////

workflow {

    read_files_ch = Channel
        .fromPath(params.infile, checkIfExists: true)
        .flatten()
        .map{file -> tuple(file.baseName, file)}

    initial_stats(read_files_ch)

    deconcat_ch = deconcat(read_files_ch).deconcatbam

    // if (params.platform == 'pacbio')
    demuxed_ch = demux(deconcat_ch)
                    .demuxfq
                    .flatten()
                    .map{file -> tuple(file.baseName, file)}

    // else if (params.platform == 'nanopore')
        // demuxed_ch = deconcat_ch

    prepro_ch = length_filter(demuxed_ch, "fasta").filteredfa

    last_ch = LAST(prepro_ch).filtmaf

    for_extract_ch = prepro_ch.join(last_ch)

    extracted_ch = extract(for_extract_ch).fastas

    sc_cluster_ch = starcode_cluster(extracted_ch).barcodeclusters

    for_lamassemble_ch = extracted_ch.join(sc_cluster_ch)

    lamassemble_cluster(for_lamassemble_ch) | final_format
}

if (params.help) {
	printHelp()
	exit 0
}

////////////////////////////// PROCESSES //////////////////////////////

// step 1: get stats on input file
process initial_stats {

    publishDir path: "$params.outdir/01_initial-stats", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), file(infile)
    // val filetype

    output: // all outputs with base_file_name in the filename (captures png histogram and txt stats)
    path "$base_file_name*"

    script:
    """
    // $STATS_SCRIPT -f $infile -o $base_file_name-initial-stats -t $filetype
    // Replace
    // This has gotta be FASTQC
    mkdir fastqc_output
    fastqc -o fastqc_output -f bam $infile
    """
}

// step 2: deconcat input file
process deconcat {

    publishDir path: "$params.outdir/02_deconcat", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), file(infile)
    // val filetype
    
    output: // captures deconcat fastq (and deconcat/demux stats files for nanopore)
    tuple val("$base_file_name"), path("$base_file_name-deconcat.bam"), emit: deconcatbam
    path "$base_file_name-stats.*", emit: deconcatstats, optional: true

    script:

    // if (params.platform == 'pacbio')
    """
    // $DECONCAT_SCRIPT -f $infile -o $base_file_name-deconcat.fastq -s $params.crfile

    // params.arrfile = "$baseDir/sequences/array_barcodes.fasta"
    skera split $infile $params.arrfile $base_file_name-deconcat.bam
    """

    // else if (params.platform == 'nanopore') // Nanopore is already demuxed, so run stats now on each FASTQ in folder
        // """
        // $DECONCAT_SCRIPT -f $infile -o $base_file_name-deconcat.fastq -s $params.crfile
        // for f in ./*-deconcat.fastq; do
            // b=`basename \$f .fastq`
            // $STATS_SCRIPT -f \$f -o \$b-stats -t $filetype
        // done
        // """
}

// step 3: demux deconcatenated file
process demux {

    publishDir path: "$params.outdir/03_demux", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), path(infile)
    // val filetype

    output: // captures demuxed fastqs and stats files for pacbio (and placeholder for nanopore)

    path("*.fastq"), emit: demuxfq, optional: true
    path "*-stats/*", emit: demuxstats, optional: true
    path "*.lima.*", emit: limacounts, optional: true

    script:
    // if (params.platform == 'pacbio') // Pacbio is ready, run stats on each FASTQ in folder
    """
    lima --same --split $infile $params.indexfile $base_file_name\\.fastq
    
    for f in ./*.fastq; do
        b=`basename \$f .fastq`
        // $STATS_SCRIPT -f \$f -o \$b-stats -t $filetype
	// Replace
    	// This has gotta be FASTQC
	mkdir "\$b-stats"
	fastqc -o \$b -f fastq \$f
    done
    """

    // else if (params.platform == 'nanopore')
        // """
        // echo "Already demultiplexed" > $base_file_name-already-demultiplexed.txt
        // """
}

// step 4: length filter demuxed files
process length_filter {

    publishDir path: "$params.outdir/04_length-filter", mode: "copy", overwrite: false

    input:  // nanopore deconcat files, pacbio deconcat/demuxed files
    tuple val(base_file_name), path(infile)
    val filetype

    output: // captures long and short filtered FASTAs
    tuple val("$base_file_name"), path("*-prepro.fasta"), emit: filteredfa
    path "*-overlong.fasta", emit: overlongfa, optional: true
    path "*-stats.*", emit: filteredstats

    script: // splits each FASTQ into 2 FASTAs, below/above specified read length, then runs stats script again
    """
    n=`basename $infile .fastq`
    bioawk -c fastx '{
        if (length(\$seq) > $params.length) 
            print ">"\$name"\\n"\$seq > "'\$n'-overlong.fasta"; 
        else 
            print ">"\$name"\\n"\$seq > "'\$n'-prepro.fasta"
        }' $infile

    for f in ./*-prepro.fasta; do
        b=`basename \$f .fasta`
        $STATS_SCRIPT -f \$f -o \$b-stats -t $filetype
    done
    """
}

// step 5: Run LAST on preprocessed files, filter output
process LAST {

    publishDir path: "$params.outdir/05_LAST", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), path(infile)

    output: // outputs filtered 
    tuple val("$base_file_name"), path ("*-filt.maf"), emit: filtmaf
    path "*-raw.maf", emit: maf
    path "*-summary.txt", emit: mafsummary

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

    $SUMMAF_SCRIPT -f $infile -m $base_file_name-raw.maf -o $base_file_name-maf-summary.txt

    $FILTERMAF_SCRIPT -i $base_file_name-raw.maf -o $base_file_name-filt.maf
    """
}

// step 6: Extract genes and barcodes
process extract {

    publishDir path: "$params.outdir/06_extract", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), path(infile_fasta), path(infile_maf)

    output:
    tuple val("$base_file_name"), path("*_barcodes.fasta"), path("*_genes.fasta"), emit: fastas
    path "*_*.tsv", emit: tsvcounts

    script:
    """
    $EXTRACT_SCRIPT -f $infile_fasta -m $infile_maf -o $base_file_name
    """
}

//step 7: Cluster barcodes using Starcode
process starcode_cluster {

    publishDir path: "$params.outdir/07_starcode", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), path(infile_barcodes), path(infile_genes)

    output:
    tuple val("$base_file_name"), path("*_clustered.txt"), emit: barcodeclusters

    script:
    """
    // $STARCODE_LOCATION -i $infile_barcodes -o $base_file_name-barcode_clustered.txt --sphere -d 1 --print-clusters --seq-id
    starcode -i $infile_barcodes -o $base_file_name-barcode_clustered.txt --sphere -d 1 --print-clusters --seq-id
    """
}

//step 8: Cluster genes using lamassemble
process lamassemble_cluster {

    publishDir path: "$params.outdir/08_lamassemble", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), path(infile_barcodes), path(infile_genes), path(infile_barcodes_clustered)

    output:
    tuple val("$base_file_name"), path("*consensus.fasta"), emit: consensusfa

    script:
    """
    $LAMASSEMBLE_SCRIPT -f $infile_genes -s $infile_barcodes_clustered -o $base_file_name-consensus.fasta -t $base_file_name-temp
    """
}

//step 9: Format final output
process final_format {

    publishDir path: "$params.outdir/09_final_output", mode: "copy", overwrite: false

    input:
    tuple val(base_file_name), path(infile)

    output:
    path "*.csv"

    script:
    """
    $FINALFORMAT_SCRIPT -f $infile -o $base_file_name-final.csv
    """
}

////////////////////////////// FUNCTIONS //////////////////////////////
def printHelp() 
{
    log.info"""\
    --infile: Path to the raw FASTQ files. If sending multiple FASTQs at once (as for Oxford Nanopore data), use pattern matching to capture files. (e.g. /folder/data/nanopore/barcode0*d_test.fastq)
    --outdir: Output directory for all results files. Will be populated with subfolders containing outputs for each process step. Default is <current working directory>/results/<run start timestamp>-results
    --arrfile: Path to FASTA file containing PacBio array barcode sequences.
    --indexfile: Path to FASTA file containing library indices.
    --length: Maximum monomer length in nt. Default is 1200. Sequences longer than length will not be included in the analysis.
    --help: Prints help information.
    """
    .stripIndent()
}
