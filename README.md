# Covid variant counter

Modified from
[this script](https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py).

## Setup

1. Be sure `python` is installed.
2. Download
   [`var_counter.py`](https://github.com/istaves/covid-variant-counter/releases/download/release/var_counter.py).
3. Be sure a file with information about the variants you'd like to search for,
   called `dictionary.csv` (see [below](#variant-dictionary)), is in the same
   directory as the python script. An example is provided here:
   [`dictionary.csv`](https://github.com/istaves/covid-variant-counter/releases/download/release/dictionary.csv)

## Usage

1. Run `var_counter.py` (this can be done directly through the file explorer or
   by running `python var_counter.py` from a terminal).
2. If the script can find the file `dictionary.csv`, it will prompt for the
   directory to the data (see [below](#input-data)) you'd like to process (on
   Windows this might look something like `C:\folder1\folder2\...` otherwise it
   might look something like `/home/folder1/folder2/...`). Enter this into the
   terminal window and press `enter`.
3. The script will print a list of the output files in `.tsv` format. These will
   be in the same directory as the input files.

## Variant dictionary

The dictionary can be as long or as short as desired, depending on the number of
variants that should be searched for. The first field on each line is the
variant name (each name entered here will be a column header in the output
files, so they should be descriptive enough to be understood). The second field
is the tolerance of the search (i.e., a tolerance of `0` means that all criteria
must match in order to classify as that variant, a tolerance of `1` means that
one can be missing, etc.). The third field is a list of strings to search for
separated by spaces (` `). Any SNP that should NOT be present in the variant
should be prepended with an exclamation point (`!`). For an example,
[`dictionary.csv`](https://github.com/istaves/covid-variant-counter/releases/download/release/dictionary.csv).

## Input data

The script should be pointed to a folder that contains `.tsv` files of input
data. Currently, it:

1. Ignores all files that don't end with `_chim_rm.tsv` or `covar_deconv.tsv`,
   so don't worry about having extra files.
2. Parses metadata from the filenames, and assumes that they start with a
   2-character WWTP code followed by a 6-character `YYMMDD`-format date. For
   example, `GR220718_Michigan_H08_S92_L001_covar_deconv.tsv`.

(the `.tsv` input files should have data starting from the third row, with sequences in the first column and counts in the second column).
