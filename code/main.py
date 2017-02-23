#!/usr/bin/env python
# -*- coding: utf-8 -*-

import window as w
import extract
import seq
import fragment
import profit
import insert

if __name__ == "__main__":
    w.clean()
    #On ouvre une séquence FASTA (séquence cible)
    path = w.path_fenetre("Ouvrir un FASTA")
    seq_target = extract.sequence(path)
    print("FASTA : "+seq_target)
    #On ouvre une séquence PDB (structure support)
    path = w.path_fenetre("Ouvrir un PDB")
    seq_template = extract.extract_pdb(path)
    print("PDB : " + seq_template)
    extract.extract_backbone(path,"seq_template_backbone.pdb")
    #On télécharge les fragments de PDB s'ils sont pas déjà téléchargés
    list_fragment = fragment.download(10)
    #On transforme les fragments en fragment backboned
    list_backboned = fragment.list_backbone(list_fragment)
    #On fragmente les fichiers en peptides de 20 résidus
    total = fragment.fragmentation_bdd(list_backboned)
    w.rangement_fragment()
    #On produit un alignement entre target et template
    print("\nMeilleur alignement : ")
    align = seq.align_needle(seq_target,seq_template) 
    #Recherche les différences en alignment(Substitution/Délétion/Insertion)
    diff = seq.diff_align(align[0],align[1])
    #Recherche des extrémités des gap d'insertions
    index_I = seq.index_template_insertion(diff)
    #Recherche des extrémités des gap de délétions
    index_D = seq.index_template_deletion(diff)
    #Recherche des extrémités des substitutions
    index_X = seq.index_template_substitution(diff)
    fragment_gap = []
    taille_gap = []
    super_gap= []
    #creation des fragments du template contenant les gap d'insertions
    for i in range(0,len(index_I),2):
        name = "insertion_" + str(index_I[i]) + ".pdb"
        path = "./fragment/"
        extended_index_I = seq.extend_index('I',index_I[i:i + 2],\
                                            len(seq_template))
        fragment.fragmentation_template(extended_index_I,name,path)
        fragment_gap.append(name)
        taille_gap.append(index_I[i+1]-index_I[i])
        super_gap.append(extended_index_I)
    #creation des fragments du template contenant les gap de délétions
    for d in range(0,len(index_D),2):
        name = "deletion_" + str(index_D[d]) + ".pdb"
        path = "./fragment/"
        extended_index_D = seq.extend_index('D',index_D[d:d + 2],\
                                            len(seq_template))
        fragment.fragmentation_template(extended_index_D,name,path)
        fragment_gap.append(name)
        taille_gap.append(index_D[d+1]-index_D[d])
        super_gap.append(extended_index_D)
    #lancement de script profit en boucle pour chaque fragment et chaque gap
    #afin de trouver les meilleurs RMSD de fit
    RMSD = profit.use_profit(fragment_gap,total,super_gap,taille_gap)
    w.rangement_final()
    #Ecriture de la protéine backboned finale
    insert.PDB_final(RMSD)
    insert.rename_resi("seq_template_backbone.pdb")
    
    #Préparation des séquences pour SCWRL
    #seq_template = extract.extract_pdb("seq_template_backbone.pdb")
    #align = seq.align_needle(seq_target,seq_template)
    #diff = seq.diff_align(align[0],align[1])
    #index_X = seq.index_template_substitution(diff)
    #template_mutant = seq.prep_scrwl(seq_template,index_X)