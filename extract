#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:53:13 2015

@author: jvanneuville
"""
from Bio import SeqIO
from Bio import PDB
import os

def extract_fasta(path):
    """
    Fonction qui extrait une sequence d'un FASTA
    """
    #utilise Biopython pour extraire une séquence d'un FASTA
    sequence = SeqIO.read(path,"fasta").seq
    return str(sequence)

def extract_pdb(path):
    """
    Fonction qui extrait une sequence d'un PDB
    """
    #utilise Biopython pour extraire une séquence d'un PDB    
    structure = PDB.PDBParser().get_structure("test",path)
    peptide = PDB.PPBuilder().build_peptides(structure)
    for i,pep in enumerate(peptide):
        sequence = str(pep.get_sequence())
    return sequence
    
def extract_backbone(path,name):
    """
    Fonction qui extrait la chaine peptidique d'un PDB et l'écrit dans 
    un fichier name"
    """
    input = open(path,"r")
    output = open(name,"w")
    for line in input : 
        if line[0:6]=="ATOM  " and line[16:17] != "B" and line[21:22] == "A":
            if line[12:16] == " N  " or line[12:16] == " CA " or \
            line[12:16] == " C  " or line[12:16] == " O  ":
                #écriture d'un fichier PDB avec les atomes constitutifs de la 
                #chaine carbonnées de la protéine
                output.write(line)
    input.close()
    output.close()

def extract_fragment_code(path):
    """
    Fonction qui extrait les codes PDB d'un fichier PISCES et renvoie 
    une liste des fragments   
    """    
    file = open(path,"r")
    list = []    
    for line in file :
        list.append(line[0:4])
    return list
    
def download_pdb(pdb):  
    """
    Telecharge des PDB depuis le net
    """
    if not(os.path.isfile("archive_pdb/"+pdb+".pdb")):
        PDB.PDBList().retrieve_pdb_file(pdb,pdir = "archive_pdb")
        os.system("cd archive_pdb \n mv pdb"+pdb.lower()+".ent "+pdb+".pdb")
    
    
def sequence(path):
    """
    Fonction de renvoi d'une sequence peptidique
    """
    sequence = extract_fasta(path)
    return sequence
  
def extract_coord(atom):
    """
    Fonction qui extrait de notre fichier "backbone_output.pdb" les 
    coordonnées des Calpha correspondant a des insertions dans notre 
    alignement 
    """
    file = open("backbone_output.pdb","r")
    coord = []
    compte = 0
    #On parcourt notre fichier ligne a ligne
    for line in file :
        #Quand on trouve un Calpha on le compte
        if line[12:16] == " CA ":
            if compte == atom : 
                coord.append(float(line[30:38]))
                coord.append(float(line[38:46]))
                coord.append(float(line[46:54]))
                break
            compte += 1
    file.close()
    return coord

def RMSD(file):
    """
    Fonction qui extrait de notre fichier profit un RMSD s'il existe, sinon 
    il renvoi une valeur tres grande
    """
    input = open(file,"r")
    #On lit dans le fichier de Profit jusqu'a trouver la ligne contenant 
    #le RMSD qu'on récupere
    for line in input:
        if "RMS:" in line: 
            input.close()
            return float(line[8:13])
    input.close()
    print("probleme d'extraction de données")
    return 200

def frag_replace(path,name):
    """
    Fonction qui copie un fragment et le place dans une racine et renvoi 
    le nom de ce fichier
    """
    name_split = name.split(".")
    name = name_split[0] + "_replace." + name_split[1]
    cmd = "cp " + path+" ./" + name
    os.system(cmd)
    return name

