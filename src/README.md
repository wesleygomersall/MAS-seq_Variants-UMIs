## Scripts

For sequential instructions, see `script_order.txt`.

Detailed descriptions including usage can be found in the script files or by running `<script> -h`.

### Brief descriptions:

`deconcatenation.py` deconcatenates reads into "monomers" including the indexes, conserved regions, gene, and barcode.

`extractRegions*.py` are different methods of extracting reads and barcodes from "monomers"

`filterMaf.py` filters the multiple alignment format output from LAST to only contain records with all three conserved regions

`final_output_MSA.py` takes the output from `runLamassemble.py` to create the final output tsv

`quality_binning.py` gives a summary of barcode certainty by counting occurances of each barcode in libraries 4 and 5

`runLamassemble.py` generates a consensus sequence for the variable regions in a barcode cluster

`summarise.py` creates a summary of the number of conserved regions per read in a multiple alignment file
