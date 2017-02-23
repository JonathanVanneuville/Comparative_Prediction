# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Sep  2 19:00:10 2015

@author: jvanneuville
"""

import Tkinter as tk
import tkFileDialog as tkfd
import os

def path_fenetre(title):
    """
    Fenetre recuperant un fichier et renvoyant un chemin absolu en chaine 
    de caracteres 
    """
    rep = os.getcwd
    root = tk.Tk()
    root.withdraw()
    file = tkfd.askopenfilename(title = title, 
        initialdir = rep)
    root.destroy()
    
    return(file)

def rangement_fragment():
    """
    Fonction qui range les fragments dans un fichier fragment
    """
    cmd = "mv *.pdb fragment/"
    try :
        os.mkdir("fragment")
    except :
        print("directory \"fragment\" already exist...")
    os.system(cmd)

def rangement_final():
    """
    Fonction qui range les pdb finaux contenant les fragments fittant 
    avec les gap
    """
    os.system("mkdir fragment_final/ \nmv *_final.pdb fragment_final/")
    
def clean():
    """
    Fonction de démarrage qui supprime les pdb, les scripts et les 
    sorties Profit
    """
    os.system("rm -Rf *.pdb *.pro *.txt fragment_final")
