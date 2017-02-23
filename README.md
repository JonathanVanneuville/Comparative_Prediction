# Comparative_Prediction
A project done in Master 2 Bioinformatic (commented in French unfortunately) using a structural comparative method in Python2.7

Requiert ProFit !

Requiert Python 2.7

- Explication : 

Le sujet 3 nous demande de coder un programme de prédiction de structures de protéines par modélisation comparative

Il n'est pas complet, mais comprend un minimum qui devrait etre fonctionnel :
	
- prise en compte d'une séquence cible et d'une structure template
	
- alignement global optimal (needleman - BLOSUM62)
	
- creation d'une base de données de peptides
	
- extraction et remplacement des gap

II 
- Contenu du programme :
Fichier code : 
	
- extract.py
	
- insert.py
	
- fragment.py
	
- main.py   <=== Fichier principal
	
- profit.py
	
- seq.py
	
- window.py
Fichier param : 
	
- PISCES_bdd.txt, 		<=== bases de données
	
- myo_human.fasta		<=== sequence de la myoglobine humaine
	
- myo_human_deletion.fasta	<=== sequence de la myoglobine humaine avec une deletion
	
- myo_human_insertion.fasta 	<=== sequence de la myoglobine humaine avec une insertion
	
- 1M6C.pdb 			<=== structure de la myoglobine de porc 

Librairie :
	
- Biopython (SeqIO, PDB, pairwise2, MatrixInfo)
	
- Tkinter


III - Utilisation :

1] compiler le fichier main.py avec la commande "python main.py"

2] choisir la sequence cible (le fichier fasta dans le fichier_param)

3] choisir la structure template (le fichier pdb dans le fichier_param)

4] le programme propose de constituer la base de données (0 NON / 1 OUI) répondre 1 pour la premiere fois
