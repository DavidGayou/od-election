#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, csv, sys

DATA_DIR = "LEGISLATIVES_1958-2012-csv"

elec_par_circo = {}

def treatment_by_candidate(row, partis, results):
    winner = (None, 0)
    for parti, k in partis:
        results[parti] = row[k]
        if row[k] > winner[1]:
            winner = (parti, row[k])
    return winner[0]

def treatment_by_parti(row, partis, results):
    winner = (None, 0)
    for parti in partis:
        results[parti] = row[parti]
        if row[parti] > winner[1]:
            winner = (parti, row[parti])
    return winner[0]

listfiles = os.listdir(DATA_DIR)
listfiles.sort()
for filename in listfiles:
    filepath = os.path.join(DATA_DIR, filename)
   # LEGISLATIVES_1958-2012-csv/cdsp_legi1958t1_circ.csv
   #1986 are proportionnal election fucking up everything
    if filename.endswith('_circ.csv') and filename != 'cdsp_legi1986_circ.csv':
        annee = int(filename[9:13])
        tour = filename[13:15]
        partis = []

        with open(filepath,'r') as csvfile:
            myCsv = csv.reader(csvfile, delimiter=',')
            if annee <= 1981:
                if tour == "t1":
                    partis = myCsv.next()[7:]
            #One more field in t2
                if tour == "t2":
                    partis = myCsv.next()[8:]
            else:
                fields = myCsv.next()
                keys = [i for i, v in enumerate(fields) if "nuance" in v]
                for r in myCsv:
                    for k in keys:
                        if r[k] not in partis:
                            partis.append((r[k],fields[k+1]))

        with open(filepath,'r') as csvfile:
            csvDict = csv.DictReader(csvfile, delimiter=',')
            for row in csvDict:
                codeDepartement = row['Code département']
                circo = row['circonscription']

                if annee <= 1981 and tour == "t2" and row.get("élu premier tour", "") == 'O':
                    #Election have been settled at the first turn
                    continue

                if codeDepartement and circo :

                    if codeDepartement not in elec_par_circo:
                        elec_par_circo[codeDepartement] = {}
                    if circo not in elec_par_circo[codeDepartement]:
                        elec_par_circo[codeDepartement][circo] = {}
                    if annee not in elec_par_circo[codeDepartement][circo]:
                        elec_par_circo[codeDepartement][circo][annee] = {}
                    if tour not in elec_par_circo[codeDepartement][circo][annee]:
                        elec_par_circo[codeDepartement][circo][annee][tour] = {}
                    if 'partis' not in elec_par_circo[codeDepartement][circo][annee][tour]:
                        elec_par_circo[codeDepartement][circo][annee][tour]['partis'] = {}
                    results = elec_par_circo[codeDepartement][circo][annee][tour]['partis']

                #fileformat change after 1981
                    if annee <= 1981:
                        elec_par_circo[codeDepartement][circo][annee]["élu"] = treatment_by_parti(row, partis, results)
                    else:
                        elec_par_circo[codeDepartement][circo][annee]["élu"] = treatment_by_candidate(row, partis, results)

        if tour == "t2":
            for dep in elec_par_circo:
                for circ in elec_par_circo[dep]:
                    print annee, dep, circ, elec_par_circo[dep][circ][annee]["élu"]
#print elec_par_circo
