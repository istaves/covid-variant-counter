#!/bin/env python3
# modified from Devin Gregory https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py

import os
import sys
import csv

print("Variant Counter")
variants_dict = {}
dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
try:
    with open(dir_path + "/dictionary.csv", "r") as dictcsv:
        variants = csv.reader(dictcsv)
        next(variants)
        for line in variants:
            variants_dict[line[0]] = [int(line[1]), line[2].split()]
    print("- Successfully read variant dictionary.")
except IOError as error:
    sys.exit("- Error reading variant dictionary!")

path = input("- Enter path to files: ").replace("\\", "/")
if path[-1] != "/":
    path += "/"

WWTPs = {}
Mixed = {}
Other = {}

files = [
    file
    for file in os.listdir(path)
    if (
        (file.lower()).endswith("chim_rm.tsv")
        or (file.lower()).endswith("covar_deconv.tsv")
    )
    and not "Collected" in file
]
indexedfiles = {}
dates = [*set([file[2:8] for file in files])]
dates.sort()
for date in dates:
    indexedfiles[date] = [file for file in files if file[2:8] == date]

print("- Found data on:")
for date in dates:
    print(
        f"   {date[:2]}.{date[2:4]}.{date[4:]} from {', '.join([*set([file[:2] for file in indexedfiles[date]])])}"
    )

print("- Successfully wrote files:")
for date in dates:
    for file in indexedfiles[date]:
        in_file = open(path + file, "r")
        wwtp = file[:2]
        try:
            WWTPs[wwtp]
        except:
            WWTPs[wwtp] = {}
            for variant in variants_dict:
                WWTPs[wwtp][variant] = 0
            WWTPs[wwtp]["Mixed"] = 0
            WWTPs[wwtp]["Other"] = 0
        try:
            Mixed[wwtp]
        except:
            Mixed[wwtp] = ""
        try:
            Other[wwtp]
        except:
            Other[wwtp] = ""
        reader = csv.reader(in_file, delimiter="\t")
        next(reader)
        next(reader)
        for line in reader:
            matches = []
            for variant in variants_dict:
                check = 0
                for SNP in variants_dict[variant][1]:
                    if SNP[0] == "!":
                        if SNP[1:] in line[0]:
                            check += 1
                    elif SNP not in line[0]:
                        check += 1
                if check <= variants_dict[variant][0]:
                    matches.append(variant)
            if len(matches) > 1:
                if not "'" + line[0] + "'" in Mixed[wwtp]:
                    Mixed[wwtp] += "'" + line[0] + "', "
                try:
                    WWTPs[wwtp]["Mixed"] += float(line[1])
                except:
                    WWTPs[wwtp]["Mixed"] = float(line[1])
            elif matches:
                try:
                    WWTPs[wwtp][matches[0]] += float(line[1])
                except:
                    WWTPs[wwtp][matches[0]] = float(line[1])
            else:
                if not "'" + line[0] + "'" in Other[wwtp]:
                    Other[wwtp] += "'" + line[0] + "', "
                try:
                    WWTPs[wwtp]["Other"] += float(line[1])
                except:
                    WWTPs[wwtp]["Other"] = float(line[1])
        in_file.close()

    outfile = open(path + date + "_variant_counts.tsv", "w")
    outfile.write("Code\tDate\tNumber of Reads")
    for variant in variants_dict:
        outfile.write("\t" + variant)
    outfile.write("\tMixed\tMixed variants\tOther\tOther variants\tComments\n")
    for wwtp in WWTPs:
        total = int(sum(WWTPs[wwtp].values()))
        outfile.write(f"{wwtp}\t{date}\t{total}\t")
        for variant in variants_dict:
            outfile.write(f"{(WWTPs[wwtp][variant] / total):.3f}\t ")
        outfile.write(f"{(WWTPs[wwtp]['Mixed'] / total):.3f}\t{Mixed[wwtp]}\t")
        outfile.write(f"{(WWTPs[wwtp]['Other'] / total):.3f}\t{Other[wwtp]}\n")

    outfile.close()
    print("   " + date + "_variant_counts.tsv")


input("Press ENTER to exit...")
