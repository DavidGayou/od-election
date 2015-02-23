#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

elec_par_circo = {}

with open('result.json', 'r') as file:
    elec_par_circo = json.load(file)
    

for num_dep in elec_par_circo:
    dep = elec_par_circo[num_dep]
    for num_circo in dep:
        circo = dep[num_circo]
        resultat = []
        for num_annee in circo:
            print num_annee
            annee = circo[num_annee]
           # print annee[u'élu']
            resultat.append(annee[u'élu'])

        print "%s - %s" %(num_dep, num_circo)
        print resultat


       

    



