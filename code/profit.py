# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Sep  2 18:37:02 2015

@author: jvanneuville
"""
 
import os
import extract
import fragment

def use_profit(gap_list,bdd_list,super_gap,taille_gap):
    """
    Fonction qui écrit un script profit, fit les structures de fragments et de
    gap et renvoi les meilleurs RMSD et les noms des fichiers contenant les 
    fragments
    """
    #On initialise un RMSD tres haut
    best_RMSD = []
    #Prends tous les fragments de gap
    for gap in range(0,len(gap_list)):
        #on initialise un RMSD tres grand (200) pour notre fitting par défaut
        extremite_gap = extrem_gap(super_gap[gap])
        print(extremite_gap)
        #On écrit le fichier de script profit permettant le calcul du RMSD 
        #entre deux fragments qu'on contraint a positionner                      
        list_data_RMSD = [10,gap_list[gap],"",0,0]
        input_profit = open("script_profit.pro","w")
        zone = int(extremite_gap[1])-int(extremite_gap[0])
        #On "fit" les deux structures sur les zones correspondantes
        input_profit.write("ZONE 1-"+str(zone+1)+":"+str(extremite_gap[0])\
                            +"-"+str(extremite_gap[1])+"\n")
        if len(extremite_gap)>2 and taille_gap[gap]<13:
            zone2 = int(extremite_gap[2])-int(extremite_gap[3])
            if zone2 < 0 : 
                #Dans le cas d'une insertion le gap est négatif, pour le 
                #calcul des zones il faut inverser la valeur
                zone2 = zone2*-1
            input_profit.write("ZONE "+str(zone+2+taille_gap[gap])+"-"\
                        +str(zone+1+taille_gap[gap]+1+zone2)+":"\
                        +str(extremite_gap[2])+"-"+str(extremite_gap[3])+"\n")            
        input_profit.write("fit")
        input_profit.close()
        #Prends tous les fragments de la base de données
        for frag in bdd_list :        
            path = "fragment/"+frag
            #on lance la commande avec une reference au gap et un mobile au gap
            cmd = "profit -f script_profit.pro "+path+" "+gap_list[gap]+\
                        " > printed_profit.txt"
            os.system(cmd)
            #On recupere la donnée de RMSD et on la compare avec une 
            #précédemment existante.
            RMSD = extract.RMSD("printed_profit.txt")
            if list_data_RMSD[0] > RMSD and RMSD < 3:
                list_data_RMSD[0] = RMSD
                name_replace = extract.frag_replace(path,gap_list[gap])
                input_profit = open("script_profit_write.pro","w")
                zone = int(extremite_gap[1])-int(extremite_gap[0])
                #On "fit" les deux structures sur les zones correspondantes
                input_profit.write("ZONE "+str(extremite_gap[0])+"-"\
                                +str(extremite_gap[1])+":1-"+str(zone+1)+"\n")
                if len(extremite_gap)>2 :
                    zone2 = int(extremite_gap[3])-int(extremite_gap[2])
                    input_profit.write("ZONE "+str(extremite_gap[2])+"-"\
                                +str(extremite_gap[3])+":"\
                                +str(zone+2+taille_gap[gap])+"-"\
                                +str(zone+1+taille_gap[gap]+1+zone2)+"\n")            
                input_profit.write("fit\n")
                input_profit.write("WRITE "+name_replace)
                input_profit.close()
                #On lance la commande
                cmd = "profit -f script_profit_write.pro "+gap_list[gap]+" "\
                                +name_replace+" > result.txt"
                os.system(cmd)
                list_data_RMSD[3] = extremite_gap[0]
                #Ajoute les extremités a l'output
                if len(extremite_gap)>2:
                    list_data_RMSD[2] = fragment.perform_pdb_frag\
                                (name_replace,zone+1+taille_gap[gap]+1+zone2)
                    list_data_RMSD[4] = extremite_gap[3]
                else :
                    list_data_RMSD[2] = fragment.perform_pdb_frag\
                                (name_replace,zone+1)
                    list_data_RMSD[4] = extremite_gap[1]
        print("changing gap...")
        #Retiens le fragment a changer, le meilleur fragment de remplacement
        #et les extremités du gap
        best_RMSD.append(list_data_RMSD)
    return best_RMSD
                
  
def extrem_gap(list):
    """
    Fonction qui prend la liste des residus dans le fragment et renvoi 
    les extremités du gap
    exemple : [10,11,12,13,16,17,18,19] -> [10,13,16,19]
    """
    begin = list[0]
    #Début du gap
    result = [list[0]]
    for i in range(1,len(list)) : 
        if list[i] != begin+1 :
            #Fin de la premiere zone (avant gap)
            result.append(list[i-1])
            #Debut de la seconde zone (apres gap)
            result.append(list[i])
            #Fin de la derniere zone (apres gap)
            result.append(list[-1])
            break
        else : 
            begin = list[i]
    #Dans le cas ou les délétions insertions sont a la fin
    if len(result) == 1:
        result.append(list[-1])
    return result