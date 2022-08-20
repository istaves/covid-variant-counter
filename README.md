# Covid variant counter
Modified from https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py.

Calculates the abundancies of covid variants.

## Usage 
Download var_counter.py and dictionary.csv, and put them together in the same folder.
Run var_counter.py. The program will ask for the directory that you'd like the program to work on. It will put its output files into that directory as well.

## Variant dictionary
The dictionary can be as long or as short as desired, depending on the number of variants that should be searched for. The first field on each line is the variant name. The second field is the tolerance of the search (i.e., a tolerance of 0 means that every SNP must match in order to classify as that variant, a tolerance of 1 means that 1 SNP can be missing, etc.). The third field is a list of SNPs to search for separated by spaces (' '). Any SNP that should NOT be present in the variant should be prepended with an exclamation point ('!').
