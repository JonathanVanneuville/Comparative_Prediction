# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Sep  2 18:37:38 2015

@author: jvanneuville
"""
from Bio import pairwise2 
from Bio.SubsMat import MatrixInfo as matlist

def align_needle(target,template):
    """
    Effectue un alignement global optimal par BLOSUM62 entre la sequence target
    et template et renvoi un tuple avec l'alignement contenant le meilleur 
    score et le plus nombre de gap
    """
    #dans le cas où cout du gap < substitution
    #align = pairwise2.align.globalxx(target, template)
    #dans le cas où cout du gap > substitution - BLOSUM 62
    matrix = matlist.blosum62
    align = pairwise2.align.globaldx(target, template, matrix) 
    #on cherche l'alignement avec le plus haut score et le plus petit nombre 
    #de gap
    res = align[0]
    for i in align:
        if i[2] >= res[2] and i[4] <= res[4]:
            res = i
    print("Sequence target  : " + res[0])
    print("Sequence template: " + res[1])
    print("Score : " + str(res[2]))
    return res

def diff_align(target,template):
    """
    Crée une ligne de comparaison de séquence : - quand c'est pareil, G pour 
    un gap, X pour une substition
    """
    res = ""
    for i in range(0,len(target)): 
        if target[i] == template[i]:
            res += '-'
        elif target[i] == '-': 
            res += 'I'
        elif template[i] == '-':
            res += 'D'
        else: 
            res += 'X'
    print("Alignement       : " + res)
    return res

def index_template_insertion(seq):
    """
    Renvoi les index des Calpha de notre backbone qui prennent part dans 
    les insertions
    """
    index = []
    #Nous ne sommes initialement pas dans un gap (0 non, 1 oui)
    gap = 0
    #Le retard du décompte des index
    compte = 0
    for i in range(0,len(seq)):
        #Si on est pas dans un gap et qu'on insere et qu'on est pas au début 
        #de la séquence, on retient l'index
        if gap == 0 and seq[i] == 'I':
            if compte == 0:
                index.append(0)
            else :
                index.append(compte-1)
            compte += 1
            gap = 1
        #Si on est dans un gap et qu'on insere toujours
        elif gap == 1 and seq[i] == 'I':
            compte+=1
        #Si on est dans un gap et qu'on arrete d'insérer on retient l'index
        elif gap == 1 and seq[i] != 'D' :
            compte += 1
            index.append(compte-1)
            gap = 0
        elif seq[i] != 'D':
            compte += 1
            gap = 0
    #Si la chaine se termine par des insertions ou délétions, alors on ajoute 
    #l'extrémité du gap
    if len(index) % 2 != 0:
        index.append(len(seq)-1)
                    
                    
    print("Index de type I : ")
    print(index)
    #on renvoi les Carbones alpha du début et la fin de chaque gap
    return index

def index_template_deletion(seq):
    """
    Renvoi les index des Calpha de notre backbone qui prennent part dans 
    les délétions
    """
    index = []
    #Nous ne sommes initialement pas dans un gap (0 non, 1 oui)
    gap = 0
    #Le retard du décompte des index
    compte = 0
    for i in range(0,len(seq)):
        if gap == 0:
            if seq[i] == 'D':
                gap = 1
                index.append(compte)
            else : 
                compte += 1
        else : 
            if seq[i] != 'D':
                gap = 0
                compte += 1
                index.append(compte)
        #Si la chaine se termine par des insertions ou délétions, alors on 
        #ajoute l'extrémité du gap
    if len(index)%2 != 0:
        index.insert(-1,compte-1)
                    
                    
    print("Index de type D : ")
    print(index)
    #on renvoi les Carbones alpha du début et la fin de chaque gap
    return index
    
def index_template_substitution(seq):
    """
    Fonction qui renvoi les index des Calpha de notre backbone correspondant 
    aux substitutions
    """
    index = []
    #Le retard du décompte des index
    compte = 0
    for i in range(0,len(seq)):   
        if seq[i] != 'D':
            if seq[i] == 'X' :
                index.append(compte+1)
            compte += 1
    print("Index de type X : ")
    print(index)
    #on renvoi les Carbones alpha du début et la fin de chaque gap
    return index
def extend_index(type,list,taille):
    """
    Fonction qui renvoi une liste des gap (insertion/délétion) étendu
    """
    extend = 0
    #recupération du résidu avant et apres le gap
    #low = list[0]
    #up = list[1] 
    #on récupere les 4 résidus avant et apres si possible
    limit = 3
    if type == 'I' :
        #si on est dans une insertion on prends une extension de 2 avant 
        #et 2 apres
        modif = 1
    else : 
        modif = 0
    while(extend < limit): 
        low = list[0]
        up = list[-1]
        #tableau de 2 cases low et up faire -1 et +1 a chaque fois en 
        #comparant si on est au dessus de 0 et en dessous de la taille
        if modif:
            if low-2 >= 0 :
                list[0] = low - 2
            if up+2 <= taille:
                list[1] = up + 2
            modif = 0
        else :
            if low-1 > 0 :
                list.insert(0,low - 1)
            if up+1 <= taille:
                list.append(up + 1)            
            extend += 1
    if 0 in list :
        list.remove(0)
    return list

def prep_scrwl(seq,index):
    """
    Fonction qui met en minuscule les résidus constants et en majuscule les 
    résidus mutants 
    """
    seq = seq.lower()
    res = "" 
    flag = 0
    for char in range(0,len(seq)):
        if flag < len(index):
            residu = index[flag]
        if char == residu - 1:        
            res += seq[char].upper()
            flag += 1
        else: 
            res += seq[char]
    print("Alignement       : " + res)
    return res
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    