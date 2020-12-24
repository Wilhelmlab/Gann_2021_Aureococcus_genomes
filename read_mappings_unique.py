##determine what percent of the reads map to unique proteins found within 
##each genome 

#location C:/Users/egann/Desktop/Aureococcus_strains/scripts/read_mappings_unique.py

#imports
import os 
import csv

#get a list of all unique proteins (also this list should probably be in supplemental)
all_v_all_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/all v. all blastp'

#get all protein names 
protein_headers = []

with open(os.path.join(all_v_all_directory,'all_plus_ref.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			protein_headers.append(line.strip().split(' ')[0].strip('>'))

#strains
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','XP_']

#open and make a blast table 
blast_table = []

with open(os.path.join(all_v_all_directory,'all_v_all.txt'),'r') as f:
	for line in f:
		blast_table.append(line.strip().split('\t'))


#for each protein, make a smaller table if it is the query
#and see whether there is a subject for the other strains 
out_list = []

for protein in protein_headers:
	by_protein = []
	#make smaller blast table
	protein_table = []

	for line in blast_table:
		if line[0] == protein:
			protein_table.append(line)

	for strain in strains:
		strain_count = 0
		for line in protein_table:
			if line[1].startswith(strain):
				strain_count = strain_count + 1
		if strain_count == 0:
			by_protein.append(0)
		else:
			by_protein.append(1)

	by_protein.append(sum(by_protein))
	by_protein.insert(0,protein)

	out_list.append(by_protein)

#write to an out file 
with open(os.path.join(all_v_all_directory,'protein_counts_by_strain.txt'),'w') as o: 
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(out_list)