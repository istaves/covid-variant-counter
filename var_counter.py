    #!/bin/env python3
# modified from Devin Gregory https://github.com/degregory/Programs/blob/main/NYC_Variant_Counter.py

import os
import sys

date = "placeholder"#os.getcwd().split("/")[-1]
# rbd = receptor-binding domain?
RBD_variants_dict = {
"Alpha"     :  [0, ["N501Y", "A570D"]],
"Beta"      :   [0, ["K417N", "E484K", "N501Y"]],
"Gamma"     :   [0, ["K417T", "E484K", "N501Y"]],
"Delta"     :   [0, [["not", "K417N"], ["not", "N440K"], ["not", "S466N"], "L452R", "T478K", ]],
"Kappa"     :   [0, ["L452R", "E484Q"]],
"Lambda"    :   [0, ["L452Q", "F590S"]],
"Omicron BA.1"   :   [1, ["1251T(K417N)", "1320G(N440K)", "1336A(G446S)", ["not", "L452Q"], "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "1478G(Q493R)", "1486A(G496S)", "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", "1640A(T547K)"]],
"Omicron BA.2"   :   [0, ["1251T(K417N)", "1320G(N440K)", ["not", "G446"],["not", "L452Q"],  "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "1478G(Q493R)", ["not", "G496"], "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", ["not", "T547"]]],
"Omicron BA.2.12.1"   :   [0, ["1251T(K417N)", "1320G(N440K)", ["not", "G446"], "1355A(L452Q)", "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "1478G(Q493R)", ["not", "G496"], "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", ["not", "T547"]]],
"Omicron BA.4/5"   :   [0, ["1251T(K417N)", "1320G(N440K)", ["not", "G446"], "1355G(L452R)", "1430A(S477N)", "1433A(T478K)", "1451C(E484A)", "T1456G(F486V)", ["not", "1478G(Q493R)"], ["not", "G496"], "1493G(Q498R)", "1501T(N501Y)", "1513C(Y505H)", ["not", "T547"]]],
"L452R"     :   [0, ["L452R", ["not", "T478K"], ["not", "E484Q"], ["not", "Q498"]]],
"Theta/Mu"     :   [0, ["E484K", "N501Y", ["not", "K417"]]],
"E484K"     :   [0, ["E484K", ["not", "N501Y"], ["not", "K417"]]],
"S477N"     :   [0, ["S477N", ["not", "N501Y"], ["not", "K417"], ["not", "T478K"]]],
"WNYC1"     :   [1, ["Q498Y", "H519N", "H519K", "E484A", "S494P", "T572N"]],
"WNYC2"     :   [0, ["Q498Y", "H519N", "Q493K"]],
"WNYC3"     :   [0, ["K417T", "E484A", "Q498", "K444T"]],
"WNYC4"     :   [0, ["Q498Y", "N501T", "F486V", "Y449R"]],
"WNYC5"     :   [0, ["K417T", "E484A", "Q498", "N440E"]]
}
# wastewater treatment facilities
WWTP_dict = {   1 : [1, "CS", "CS"],
                2 : [2, "GR", "GR"],
                3 : [3, "V1", "V1"],
                4 : [4, "WB", "WB"]
}
WWTP_dict2 = {   "CS" : 1,
                "GR" : 2,
                "V1" : 3,
                "WB" : 4
}

WWTPs = {}
Mixed = {}
OmiPMs = {}
NTD_WWTPs = {}
NTD_Mixed = {}
# NTD_OmiPMs = {}

for file in os.listdir(os.getcwd()): #loops over fileNAMES in current wd
        if (file.lower()).endswith('_chim_rm.tsv') and not 'Collected' in file:
            in_file = open(file, "r")
            if "NY" in file:
                wwtp = int(file.split("_")[0].strip("NYRBDA"))
            else: 
                try:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")]
                except:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")[:-1]]
            try:
                WWTPs[wwtp]
            except:
                WWTPs[wwtp] = {"Alpha" : 0,
                                "Beta" : 0,
                                "Gamma" : 0,
                                "Delta" : 0,
                                "Kappa" : 0,
                                "Lambda" : 0,
                                "Omicron BA.1" : 0,
                                "Omicron BA.2" : 0,
                                "Omicron BA.2.12.1" : 0,
                                "Omicron BA.4/5" : 0,
                                "L452R" : 0,
                                "Theta/Mu" : 0,
                                "E484K" : 0,
                                "S477N" : 0,
                                "WNYC1" : 0,
                                "WNYC2" : 0,
                                "WNYC3" : 0,
                                "WNYC4" : 0,
                                "WNYC5" : 0,
                                "Mixed" : 0,
                                "Other" : 0
                                        }
            try:
                Mixed[wwtp]
            except:
                Mixed[wwtp] = ''
            for line in in_file:
                splitline = line.split("\t")
                try:
                    splitline[2]
                except:
                    pass
                else:
                    if not splitline[1] == "Count":
                        matches = []
                        for variant in RBD_variants_dict:
                            check = 0
                            for SNP in RBD_variants_dict[variant][1]:
                                try:
                                    if not SNP in line:
                                        check += 1
                                except:
                                    if SNP[1] in line:
                                        check += 1
                                    
                            if check <= RBD_variants_dict[variant][0]:
                                matches.append(variant)
                           
                            
                        if matches:
                            try:
                                matches[1]
                            except:
                                # print(line + " matches " + " ".join(matches))
                                try:
                                    WWTPs[wwtp][matches[0]] += float(splitline[1])
                                except:
                                    WWTPs[wwtp][matches[0]] = float(splitline[1])
                            else:
                                print(wwtp)
                                print(line + " matches " + " ".join(matches))
                                sequence = "'" + line.split("\t")[0] + "'"
                                if not sequence in Mixed[wwtp]:
                                    Mixed[wwtp] = Mixed[wwtp] + sequence + ", "
                                try:
                                    WWTPs[wwtp]["Mixed"] += float(splitline[1])
                                except:
                                    WWTPs[wwtp]["Mixed"] = float(splitline[1])

                        else:
                            # print(line + " matches " + " none ")
                            try:
                                WWTPs[wwtp]["Other"] += float(splitline[1])
                            except:
                                WWTPs[wwtp]["Other"] = float(splitline[1])
                        

            in_file.close()
        elif (file.lower()).endswith('_deconv.tsv') and not 'Collected' in file:
            in_file = open(file, "r")
            if "NY" in file:
                wwtp = int(file.split("_")[0].strip("NYRBDA"))
            else:
                try:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")]
                except:
                    wwtp = WWTP_dict2[file.split("_")[0].strip("0d")[:-1]]
            try:
                WWTPs[wwtp]
            except:
                WWTPs[wwtp] = {"Alpha" : 0,
                                "Beta" : 0,
                                "Gamma" : 0,
                                "Delta" : 0,
                                "Kappa" : 0,
                                "Lambda" : 0,
                                "Omicron BA.1" : 0,
                                "Omicron BA.2" : 0,
                                "Omicron BA.2.12.1" : 0,
                                "Omicron BA.4/5" : 0,
                                "L452R" : 0,
                                "Theta" : 0,
                                "E484K" : 0,
                                "S477N" : 0,
                                "WNYC1" : 0,
                                "WNYC2" : 0,
                                "WNYC3" : 0,
                                "WNYC4" : 0,
                                "WNYC5" : 0,
                                "Mixed" : 0,
                                "Other" : 0
                                        }
            try:
                Mixed[wwtp]
            except:
                Mixed[wwtp] = ''
            
            for line in in_file:
                splitline = line.split("\t")
                try:
                    splitline[2]
                except:
                    pass
                else:
                    if not splitline[1] == "Count":
                        matches = []
                        for variant in RBD_variants_dict:
                            check = 0
                            for SNP in RBD_variants_dict[variant][1]:
                                try:
                                    if not SNP in line:
                                        check += 1
                                except:
                                    if SNP[1] in line:
                                        check += 1
                                    
                            if check <= RBD_variants_dict[variant][0]:
                                matches.append(variant)
                                
                                   
                        if matches:
                            try:
                                matches[1]
                            except:
                                # print(line + " matches " + " ".join(matches))
                                try:
                                    WWTPs[wwtp][matches[0]] += float(splitline[1])
                                except:
                                    WWTPs[wwtp][matches[0]] = float(splitline[1])
                            else:
                                print(wwtp)
                                print(line + " matches " + " ".join(matches))
                                sequence = "'" + line.split("\t")[0] + "'"
                                if not sequence in Mixed[wwtp]:
                                    Mixed[wwtp] = Mixed[wwtp] + sequence + ", "
                                try:
                                    WWTPs[wwtp]["Mixed"] += float(splitline[1])
                                except:
                                    WWTPs[wwtp]["Mixed"] = float(splitline[1])

                        else:
                            # print(line + " matches " + " none ")
                            try:
                                WWTPs[wwtp]["Other"] += float(splitline[1])
                            except:
                                WWTPs[wwtp]["Other"] = float(splitline[1])

            in_file.close()


outfile = open(date+"RBD_variant_counts.tsv", "w")
outfile.write("Code\tWWTP\tBorough\tDate\tVirus Concentration (virus copies/L)\tNumber of Reads\tFlow rate (to be provided by DEP)\tiSeq/MiSeq\tSRA Accession\tAlpha N501Y+A570D")
outfile.write("\tBeta K417N+E484K+N501Y\tGamma K417T+E484K+N501Y\tDelta L452R+T478K")
outfile.write("\tKappa L452R+E484Q\tLambda L452R+F590S\tOmicron BA.1\tOmicron BA.2\tOmicron BA.2.12.1\tOmicron BA.4/5")
outfile.write("\tL452R (not T478K E484Q or Q498)\tTheta/Mu E484K N501Y (not K417)\tE484K (not K417 or N501Y)\tS477N (not K417 T478K or N501Y)")
outfile.write("\tWNY1 Family Q498Y H519 E484A\tWNY2 Family Q498Y H519N Q493K\tWNY3 Family K417T E484A Q498 K444T\tWNY4 Family Q498Y N501T F486V Y449R\tWNY5 Family K417T E484A Q498 N440E\tMixed\tOthers\tRBD comments\n")

for wwtp in range(1, 5):
    # print(wwtp)
    try:
        # print(WWTPs[wwtp])
        total = int(sum(WWTPs[wwtp].values()))
        outfile.write(f"{WWTP_dict[int(wwtp)][0]}\t{WWTP_dict[int(wwtp)][1]}\t{WWTP_dict[int(wwtp)][2]}\t{date}\t\t{total}\t\tMiSeq\t\t")
        for variant in WWTPs[wwtp]:
            outfile.write(f"{(WWTPs[wwtp][variant] / total):.3f}\t ")
        
        outfile.write(Mixed[wwtp])
    except:
        outfile.write(f"{WWTP_dict[int(wwtp)][0]}\t{WWTP_dict[int(wwtp)][1]}\t{WWTP_dict[int(wwtp)][2]}\t{date}\t\tNR\t\tMiSeq\t\t")
        for variant in RBD_variants_dict:
            outfile.write("NR\t ")
    outfile.write("\n")
outfile.write("\n")
outfile.write("Code\tWWTP\tBorough\tDate\tOmicron Overlap\n")
for wwtp in OmiPMs:
    total = int(sum(WWTPs[wwtp].values()))
    outfile.write(f"{WWTP_dict[int(wwtp)][0]}\t{WWTP_dict[int(wwtp)][1]}\t{WWTP_dict[int(wwtp)][2]}\t{date}\tOverlap\t% abundance\n")
    for overlap in OmiPMs[wwtp]:
        outfile.write(f"\t\t\t\t{overlap}\t{(OmiPMs[wwtp][overlap] / total):.3f}\n")
    
outfile.close()

# ## NTD out
# outfile = open(date+"NTD_variant_counts.tsv", "w")
# outfile.write("Code\tWWTP\tBorough\tDate\tVirus Concentration (virus copies/L)\tNumber of Reads\tFlow rate (to be provided by DEP)\tiSeq/MiSeq\tSRA Accession\tAlpha 203-208Del 429-431Del")
# outfile.write("\tBeta D80A D215G\tGamma D138Y R190S\tDelta 425A(G142D) 467-472Del(E156G)")
# outfile.write("\tLambda G75V T76I\tOmicron BA.1\tOmicron BA.2")
# outfile.write("\tMixed\tOthers\tNTD comments\n")

# for wwtp in range(1, 15):
    # # print(wwtp)
    # try:
        # # print(NTD_WWTPs[wwtp])
        # total = int(sum(NTD_WWTPs[wwtp].values()))
        # outfile.write(f"{WWTP_dict[int(wwtp)][0]}\t{WWTP_dict[int(wwtp)][1]}\t{WWTP_dict[int(wwtp)][2]}\t{date}\t\t{total}\t\tMiSeq\t\t")
        # for variant in NTD_WWTPs[wwtp]:
            # outfile.write(f"{(NTD_WWTPs[wwtp][variant] / total):.3f}\t ")
        
        # outfile.write(NTD_Mixed[wwtp])
    # except:
        # outfile.write(f"{WWTP_dict[int(wwtp)][0]}\t{WWTP_dict[int(wwtp)][1]}\t{WWTP_dict[int(wwtp)][2]}\t{date}\t\tNR\t\tMiSeq\t\t")
        # for variant in NTD_variants_dict:
            # outfile.write("NR\t ")
    # outfile.write("\n")
# # outfile.write("\n")
# # outfile.write("Code\tWWTP\tBorough\tDate\tOmicron Overlap\n")
# # for wwtp in NTD_OmiPMs:
    # # total = int(sum(NTD_WWTPs[wwtp].values()))
    # # outfile.write(f"{WWTP_dict[int(wwtp)][0]}\t{WWTP_dict[int(wwtp)][1]}\t{WWTP_dict[int(wwtp)][2]}\t{date}\tOverlap\t% abundance\n")
    # # for overlap in NTD_OmiPMs[wwtp]:
        # # outfile.write(f"\t\t\t\t{overlap}\t{(NTD_OmiPMs[wwtp][overlap] / total):.3f}\n")
    
# outfile.close()
