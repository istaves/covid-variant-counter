#!/bin/env python3
# modified from Devin Gregory https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py

import os
import sys
import csv
print("Variant Counter")
variants_dict = {}

try:
    with open("dictionary.csv", "r") as dictcsv:
        variants = csv.reader(dictcsv)
        next(variants)
        for line in variants:
            variants_dict[line[0]] = [int(line[1]),line[2].split()]
    print("- Successfully read variant dictionary.") 
except IOError as error:
    print("- Error reading variant dictionary!")
# print(variants_dict)

path = input("- Enter path to files: ").replace("\\","/")
if path[-1] != '/':
    path += '/'

WWTPs = {}
Mixed = {}

files = [file for file in os.listdir(path) if (file.lower()).endswith('chim_rm.tsv') and not 'Collected' in file]
indexedfiles = {}
dates = [*set([file[2:8] for file in files])]
dates.sort()
for date in dates:
    indexedfiles[date] = [file for file in files if file[2:8]==date]

print("- Found data on:")
for date in dates:
    print(f"   {date[:2]}.{date[2:4]}.{date[4:]} from WWTPs {', '.join([file[:2] for file in indexedfiles[date]])}")

print("- Successfully wrote files:")
for date in dates:
    for file in indexedfiles[date]: #loops over fileNAMES in current wd
        in_file = open(path + file, "r")
        wwtp = file[:2]
        try:
            WWTPs[wwtp]
        except:
            WWTPs[wwtp] = {}
            for variant in variants_dict:
                WWTPs[wwtp][variant] = 0
        try:
            Mixed[wwtp]
        except:
            Mixed[wwtp] = ''
        for line in in_file:

            reader = csv.reader(in_file,delimiter="\t")
            next(reader)
            next(reader)
            for line in reader:
                matches = []
                for variant in variants_dict:
                    check = 0
                    for SNP in variants_dict[variant][1]:
                        if SNP[0]=="!" and SNP[1:] in line[0]:
                            check += 1
                        elif SNP not in line[0]:
                            check += 1
                        if check <= variants_dict[variant][0]:
                            matches.append(variant)
                if len(matches) > 1:
                    #print(wwtp)
                    #print(line + " matches " + " ".join(matches))
                    if not "'" + line[0] + "'" in Mixed[wwtp]:
                        Mixed[wwtp] = "'" + line[0] + "', "
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
                    # print(line + " matches " + " none ")
                    try:
                        WWTPs[wwtp]["Other"] += float(line[1])
                    except:
                        WWTPs[wwtp]["Other"] = float(line[1])
                        
        in_file.close()


    outfile = open(path+date+"_variant_counts.tsv", "w")
    outfile.write("WWTP\tDate\tVirus Concentration (virus copies/L)\tNumber of Reads\tFlow rate (to be provided by DEP)\tiSeq/MiSeq\tSRA Accession\tAlpha N501Y+A570D")
    outfile.write("\tBeta K417N+E484K+N501Y\tGamma K417T+E484K+N501Y\tDelta L452R+T478K")
    outfile.write("\tKappa L452R+E484Q\tLambda L452R+F590S\tOmicron BA.1\tOmicron BA.2\tOmicron BA.2.12.1\tOmicron BA.4/5")
    outfile.write("\tL452R (not T478K E484Q or Q498)\tTheta/Mu E484K N501Y (not K417)\tE484K (not K417 or N501Y)\tS477N (not K417 T478K or N501Y)")
    outfile.write("\tWNY1 Family Q498Y H519 E484A\tWNY2 Family Q498Y H519N Q493K\tWNY3 Family K417T E484A Q498 K444T\tWNY4 Family Q498Y N501T F486V Y449R\tWNY5 Family K417T E484A Q498 N440E\tMixed\tOthers\tRBD comments\n")

    for wwtp in WWTPs:
        total = int(sum(WWTPs[wwtp].values()))
        outfile.write(f"{wwtp}\t{date}\t\t{total}\t\tMiSeq\t\t")
        for variant in WWTPs[wwtp]:
            outfile.write(f"{(WWTPs[wwtp][variant] / total):.3f}\t ")
        
        outfile.write(Mixed[wwtp])
        outfile.write("\n")
    
    outfile.close()
    print("   "+date+"_variant_counts.tsv")


input("Press ENTER to exit...")
