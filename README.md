# Covid variant counter

Modified from
[this script](https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py).

## Setup

### Windows
On Windows, you can download a portable version (i.e., a `.exe` file that can be run without installation or other requirements) from the [latest release](https://github.com/istaves/covid-variant-counter/releases/latest).

### MacOS and other systems
For now, there is no package on systems other than Windows. In the meantime, you can download and run the `.py` file (from the [latest release](https://github.com/istaves/covid-variant-counter/releases/latest)) as long as Python is installed.

## Usage

1. Run the program (either the Windows executable or Python script, as described above).
2. Press "Choose dictionary file:" and browse to the dictionary file (see [Variant Dictionary](#variant-dictionary)). Usually you won't have to do this step, since the program will remember the dictionary file that was used on the last run.
3. Press "Choose input directory:" and navigate to the directory with the input files you'd like to process (see [Input Data](#input-data))
4. Press "Save output as:" to tell the program where to save the output, in `.tsv` format.
5. Press "Run".

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

## Notes

* The program will create a file in its directory called `pref.dat`. All this does is remember the last dictionary file that was used, so it doesn't need to be chosen every time - so don't worry if it gets deleted.
