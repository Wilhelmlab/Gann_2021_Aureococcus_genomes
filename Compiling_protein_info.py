#compile all data from eggNOG, blastKOALA, 
#blastp against the uniprot/swiss prot/and 
#blast against the reference CCMP1984 genome 

#imports 
import os 
import csv 

#directories 
blastKOALA_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/blastKOALA_results'
eggNOG_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/eggNOG'
uniprot_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/uniprot_blastp'
blastp_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/blastp'
parent_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/'

#open files and make data tables 
protein_names = []
blastKOALA_table = []
eggNOG_table = []
uniprot_table = []
blastp_table = []

with open(os.path.join(parent_directory,'all_plus_ref.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			protein_names.append(line.strip().split(' ')[0].strip('>'))

with open(os.path.join(blastKOALA_directory,'blastKOALA_all.txt'),'r') as f:
	for line in f: 
		blastKOALA_table.append(line.strip().split('\t'))

with open(os.path.join(eggNOG_directory,'eggNOG_table.txt'),'r') as f: 
	for line in f: 
		eggNOG_table.append(line.strip().split('\t'))

with open(os.path.join(uniprot_directory,'all_proteins_uniprot_data.txt'),'r') as f:
	for line in f: 
		uniprot_table.append(line.strip().split('\t'))

with open(os.path.join(blastp_directory,'all_v_all_full_table.txt'),'r') as f: 
	for line in f: 
		blastp_table.append(line.strip().split('\t'))


#pull all data from each type of file
for protein in protein_names:
	out_line = [protein]
	#uniprot table first
	for line in uniprot_table:
		if line[0] == protein:
			#if len(line) == 1:
				if len(line) == 1:
					out_line.append('-')
					out_line.append('-')
				elif len(line) != 1:
					out_line.append(line[1])
					out_line.append(line[2])
	print(out_line)
	