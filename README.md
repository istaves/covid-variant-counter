# Covid variant counter

Modified from
[this script](https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py).

## Setup

1. Be sure `python` is installed.
2. Download
   [`var_counter.py`](https://github.com/istaves/covid-variant-counter/releases/download/release/var_counter.py).
3. Be sure a file with information about the variants you'd like to search for,
   called `dictionary.csv` (see below), is in the same directory as the python
   script. An example is provided here:
   [`dictionary.csv`](https://github.com/istaves/covid-variant-counter/releases/download/release/dictionary.csv)

## Usage

1. Run `var_counter.py` (this can be done directly through the file explorer or
   by running `python var_counter.py` from a terminal).
2. If the script can find the file `dictionary.csv`, it will prompt for the directory to the data you'd like to process.

## Variant dictionary

The dictionary can be as long or as short as desired, depending on the number of
variants that should be searched for. The first field on each line is the
variant name. The second field is the tolerance of the search (i.e., a tolerance
of 0 means that every SNP must match in order to classify as that variant, a
tolerance of 1 means that 1 SNP can be missing, etc.). The third field is a list
of SNPs to search for separated by spaces (' '). Any SNP that should NOT be
present in the variant should be prepended with an exclamation point ('!').
