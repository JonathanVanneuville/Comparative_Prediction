# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Tue Sep  8 14:09:51 2015

@author: jvanneuville
"""

import extract
import window as w
import os
  
def download(nb):
    """
    Fonction qui demande et lance le téléchargement d'une banque de 
    données de structure PDB
    """
    boolean_test = input("Voulez vous telecharger une banque de données ? \
                        [1/0]")
    list_fragment = []
    if boolean_test :
        path = w.path_fenetre("Ouvrir un fichier de liste de fragments")
        list_fragment = extract.extract_fragment_code(path)
        list_fragment.pop(0) #On enleve l'en-tete du fichier
        download = 0
        for code in list_fragment :
            if download < nb :            
                extract.download_pdb(code)
            else :
                break
            download += 1
    else : 
        list_dir = os.listdir("archive_pdb/")
        for i in list_dir:
            list_fragment.append(i.split(".")[0])
    return list_fragment[0:nb]


def list_backbone(list):
    """
    Fonction qui prend une liste de code PDB et renvoi des fichier PDB avec 
    juste leurs backbone
    """
    list_backboned = []
    for code in list:
        path = "archive_pdb/" + code + ".pdb"
        name = code+"_backbone.pdb"
        extract.extract_backbone(path,name)
        list_backboned.append(name)
    return list_backboned

def fragmentation_bdd(list):
    """
    Fonction qui prend une liste de pdb backboned et qui écrit dans un fichier 
    pdb séparé les 80 atomes (4 atomes * 20 résidus) qui composent le fragment
    """
    #Futur nom du fichier pdb
    name_number = 1
    list_output = []
    for file in list:
        #on ouvre le fichier pdb backboned (pour chaque protéine)
        input = open(file,"r")
        list_input = []      
        for line in input :
            #on crée un tableau qui contient chaque ligne du fichier
            list_input.append(line)
        for i in range(0,len(list_input)-80,4) :
            name = str(name_number)+"_"+file
            #creation d'un fichier qu'on va écrire
            output = open(name,"w")
            #il va contenir les 80 premieres lignes (N,C,O,CA) de chaque 
            #résidu > 20 résidus
            for j in range(0,80):
                residu_nb = j/4+1
                #on écrit, mais on renomme le numéro des résidus 1->20
                if len(str(residu_nb)) == 1 :
                    write_line = list_input[i+j].replace(
                        list_input[i+j][22:26],
                        "   "+str(residu_nb))
                else : 
                    write_line = list_input[i+j].replace(
                        list_input[i+j][22:26],
                        "  "+str(residu_nb))
                output.write(write_line)
            output.close()
            #le fichier suivant aura un autre nom
            name_number += 1
            list_output.append(name)
            
        input.close()
    return list_output


    
def fragmentation_template(list,name,path):
    """
    Fonction qui crée des fragments de template entourant les gap 
    d'insertion et de délétions
    """
    input_name = path+"seq_template_backbone.pdb"
    input = open(input_name,"r")
    input_list = []
    output = open(name,"w")
    for line in input :
        input_list.append(line)
    for residu in list:
        atom = 0
        while(atom < 4):
            if residu == "0" :
                output.write(input_list[4*(residu)+atom])
            else :
                output.write(input_list[4*(residu-1)+atom])
            atom += 1
    input.close()
    output.close()
    
def perform_pdb_frag(name,extrem):
    """
    Fonction qui écrit un fichier pdb contenant le fragments raccourcis 
    allant de 1 a l'extrémité du gap
    """
    input = open(name,"r")
    name = name.split(".")
    name_output = name[0]+"_final."+name[1]
    output = open(name_output,"w")
    file = []
    for line in input :
        file.append(line)
    for index in range(0,extrem*4) :
        output.write(file[index])
    input.close()
    output.close()
    return name_output

