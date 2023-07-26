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

The dictionary takes the form of a table. The column headers (entries in the first row)
are the variant names and the row headers (in the first colomn) are positions.

In the approprate cells...
* an exclamation point (`!`) means that there should be 
no mutation from the wild type
* a single-letter amino acid code (e.g., `R`) means that there should be a **mutation from the wild type**
to the indicated amino acid
* an exclamation point and a single-letter code (e.g., `!R`) means that there should not be
a **mutation from the wild type** to the indicated amino acid (i.e., there might be no mutation or
a different mutation)
* an asterisk (`*`) means that there should be a (any) mutation
...at that position (in the row header) in order for a sequence to be identified as that variant
(in the column header). A space (` `) means that position is not necessary to identify that variant.

For example, in the table below, in order for a sequence to be identified as Variant X, at position
339 the amino acid must be **mutated** from the wild type to aspartic acid, and at positions 356 and 368
the amino acid must be the same as the wild type. In order for a sequence to be identified as Variant Y,
at position 339 the amino acid must be changed from the wild type, and at position 368 there must not
be a **mutation** to isoleucine. In order for a sequence to be identified as Variant Z, there must be
a **mutation** to histidine at position 339, a **mutation** to threonine at position 356, and at
position 368 there must not be a **mutation** to isoleucine.

|       | X | Y | Z |
|-------|---|---|---|
| 339   | D | * | H |
| 356   | ! |   | T |
| 368   | ! |!I |!I |

(Of course, more rows would be necessary to properly differentiate between X and Y, and Y and Z).

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
