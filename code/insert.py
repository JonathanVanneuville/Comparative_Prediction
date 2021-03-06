# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:06:06 2015

@author: jvanneuville
"""

def PDB_final(list):
    """
    Fonction qui recopie les meilleurs fragments dans le fichier 
    PDB de la protéine
    """
    #on ouvre le fichier de protéine backboned
    recup_prot = open("./fragment/seq_template_backbone.pdb","r")
    file = []
    inser = []
    for line in recup_prot : 
        file.append(line)
    recup_prot.close()   
    #on ouvre le fichier de l'inser protéique
    for gap in list :
        extrem_low = gap[3]
        extrem_up = gap[4]
        #on supprime les lignes correspondant au gap dans le tableau
        for index in range(extrem_low*4,extrem_up*4):
            file.pop(extrem_low*4)
        
        #on recupere les coordonnées a inserer        
        inser_frag = open("./fragment_final/"+gap[2],"r")        
        for line in inser_frag : 
            inser.append(line)
        inser_frag.close()
        #on insert les données dans le tableau
        for index in range(0,len(inser))[::-1] :
            file.insert(extrem_low*4,inser[index])   
         
    #Ecriture du fichier backboned final
    final_prot_backbone = open("seq_template_backbone.pdb","w")
    for line in file : 
        final_prot_backbone.write(line)
    final_prot_backbone.close()
    
def rename_resi(file):
    """
    Fonction qui sert a changer le nom des résidus
    """
    input = open(file,"r")
    file = []
    output = open("seq_template_final.pdb","w")
    flag = 0
    for line in input:
        file.append(line)
    for index in range(0,len(file)):
        residu_nb = flag/4 + 1
        if len(str(residu_nb)) == 1 : 
            output_line = file[index].replace(file[index][22:26],"   "\
                                                +str(residu_nb))
        elif len(str(residu_nb)) == 2 : 
            output_line = file[index].replace(file[index][22:26],"  "\
                                                +str(residu_nb))
        else : 
            output_line = file[index].replace(file[index][22:26]," "\
                                                +str(residu_nb))
        flag += 1
        output.write(output_line)
    input.close()
    output.close()