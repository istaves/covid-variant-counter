#!/bin/env python3
# modified from Devin Gregory https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py

import os
import sys
import csv

### READ IN VARIANT DICTIONARY ###
print("Variant Counter")
variants_dict = {}
if getattr(sys, 'frozen', False):
    dir_path = os.path.dirname(os.path.realpath(sys.executable)).replace("\\", "/")
elif __file__:
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
else:
    sys.exit("- Error getting current directory")

try:
    with open(dir_path + "/dictionary.csv", "r") as dictcsv:
        variants = csv.reader(dictcsv)
        next(variants)
        for line in variants:
            variants_dict[line[0]] = [int(line[1]), line[2].split()]
    print("- Successfully read variant dictionary.")
except IOError as error:
    sys.exit("- Error reading variant dictionary!")

### PROMPT FOR INPUT DIRECTORY ###
path = input("- Enter path to files: ").replace("\\", "/")
if path[-1] != "/":
    path += "/"

rows = {}
header = (
    ["Code", "Date", "Number of Reads"]
    + [var for var in variants_dict]
    + ["Mixed", "Mixed variants", "Other", "Other variants"]
)

### GET LIST OF VALID INPUT FILES ###
files = [
    file
    for file in os.listdir(path)
    if (
        (file.lower()).endswith("chim_rm.tsv")
        or (file.lower()).endswith("covar_deconv.tsv")
    )
    and not "Collected" in file
]

ids = sorted([*set([f[:8] for f in files])])
for i in ids:
    rows[i] = {}
    rows[i]["Code"] = i[:2]
    rows[i]["Date"] = i[2:8]
    rows[i]["Number of Reads"] = 0
    for var in variants_dict:
        rows[i][var] = 0
    rows[i]["Mixed"] = 0
    rows[i]["Mixed variants"] = ""
    rows[i]["Other"] = 0
    rows[i]["Other variants"] = ""

print("- Found data on:")
for date in sorted([*set([i[2:8] for i in ids])]):
    print(
            f"    {date[:2]}.{date[2:4]}.{date[4:]} from {', '.join([i[:2] for i in ids if i[2:] == date])}"
    )

### PROCESS DATA ###
for file in files:
    in_file = open(path + file, "r")
    id = file[:8]
    reader = csv.reader(in_file, delimiter="\t")
    next(reader)
    next(reader)
    for line in reader:  # search for matches
        matches = []
        for var in variants_dict:
            check = 0
            for SNP in variants_dict[var][1]:
                if SNP[0] == "!":
                    if SNP[1:] in line[0]:
                        check += 1
                elif SNP not in line[0]:
                    check += 1
            if check <= variants_dict[var][0]:
                matches.append(var)
        if len(matches) > 1:  # if matches multiple variants
            rows[id]["Mixed"] += float(line[1])
            if not "'" + line[0] + "'" in rows[id]["Mixed variants"]:
                rows[id]["Mixed variants"] += "'" + line[0] + "', "
        elif matches:  # if matches one variant, classify accordingly
            rows[id][matches[0]] += float(line[1])
        else:  # if matches no variants, classify as "other" and record sequence data
            rows[id]["Other"] += float(line[1])
            if not "'" + line[0] + "'" in rows[id]["Other variants"]:
                rows[id]["Other variants"] += "'" + line[0] + "', "
        rows[id]["Number of Reads"] += float(line[1])
    in_file.close()

### WRITE OUTPUT FILES ###
with open(path + "variant_counts.tsv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=header, delimiter="\t")
    writer.writeheader()
    for id in rows:
        for var in [i for i in variants_dict] + ["Mixed", "Other"]:
            rows[id][var] = round((rows[id][var] / rows[id]["Number of Reads"]), 3)
        writer.writerow(rows[id])

print("- Successfully wrote file variant_counts.tsv")

input("Press ENTER to exit...")
