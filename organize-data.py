#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import os

DATA_DIR = "LEGISLATIVES_1958-2012-csv"

elec_par_circo= {}

def treatment_by_parti(row,partis):
    #print "====================================="
    if 'partis' not in elec_par_circo[codeDepartement][circo][annee][tour]:
        elec_par_circo[codeDepartement][circo][annee][tour]['partis'] = {}

    myPartis = elec_par_circo[codeDepartement][circo][annee][tour]['partis']
    for parti in partis:
        myPartis[parti] = row[parti]

    #print myPartis
        


for filename in os.listdir(DATA_DIR):
    filepath = os.path.join(DATA_DIR, filename)
   # LEGISLATIVES_1958-2012-csv/cdsp_legi1958t1_circ.csv
   #1986 are proportionnal election fucking up everything
    if filename.endswith('_circ.csv') and filename != 'cdsp_legi1986_circ.csv':
        #print filename
        #print "*************************************"
        annee = int(filename[9:13])
        #print annee
        tour = filename[13:15]
        #print tour
        partis = {}

        if annee <= 1981:
            with open(filepath,'r') as csvfile:
                myCsv = csv.reader(csvfile, delimiter=',')
                partis = myCsv.next()[7:]

        with open(filepath,'r') as csvfile:

            csvDict = csv.DictReader(csvfile, delimiter=',') 
            for row in csvDict:
                codeDepartement = row['Code département']
                #print codeDepartement
                circo = row['circonscription']
                #print circo
                
                if codeDepartement and circo :

                    if codeDepartement not in  elec_par_circo:
                        elec_par_circo[codeDepartement] = {}
                    if circo not in elec_par_circo[codeDepartement]:
                        elec_par_circo[codeDepartement][circo] = {}
                    if annee not in elec_par_circo[codeDepartement][circo]:
                        elec_par_circo[codeDepartement][circo][annee]={}
                    if tour not in elec_par_circo[codeDepartement][circo][annee]:
                        elec_par_circo[codeDepartement][circo][annee][tour]={}


                    #fileformat change after 1981
                    
                    if annee <= 1981:
                        treatment_by_parti(row,partis)


                    #if 'partis' not in elec_par_circo[codeDepartement][circo][annee][tour]:
                    #    elec_par_circo[codeDepartement][circo][annee][tour]['partis'] = {}

                    #for parti in row.keys()[7:]:
                    #    print parti
                    #elec_par_circo[codeDepartement][circo][annee][tour]['partis']
                
                
               
#print elec_par_circo
