#!/bin/bash
#SBATCH --job-name=nextf_pb
#SBATCH --output=nextflow_pb_%j.out
#SBATCH --error=nextflow_pb_%j.err
#SBATCH --time=5-00:00:00        
#SBATCH --cpus-per-task=8        
#SBATCH --mem=100G                
#SBATCH --partition=bgmp      


# Run Nextflow with Apptainer


nextflow run main.nf -with-apptainer pb.sif \
		  --infile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/m64047_230306_210601.ccs.bam \
			--indexfile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/barcodes.fasta \
			--arrfile /projects/bgmp/shared/groups/2024/novel-fluor/shared/rawdata/RED/PacBio_MAS_ISO_seq_GC3F_6761/mas16_primers.fasta \
		  --crfile /projects/bgmp/malm/bioinfo/pb-testing1/sequences/conserved_regions.fasta \ 

