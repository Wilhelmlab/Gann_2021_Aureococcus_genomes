#Pull out the selenoproteins top hits from

#imports 
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Selenoproteins'

#get all subjects from db fasta file 
fasta_dict = dict()
key = ""

with open(os.path.join(directory, 'Selenoprotein_hit_chunk.fasta'),'r') as f: 
	for line in f: 
		if line.startswith('>'):
			key = line.strip().split(' ')[0].strip('>')
			fasta_dict[key] = ""
		else:
			fasta_dict[key] += line.strip()


for key in fasta_dict:
	print(key)
	n = 3
	if 'TGA' in fasta_dict[key]:
		print('in string')
	key_data = [fasta_dict[key][i:i+n] for i in range(0, len(fasta_dict[key]), n)]
	if 'TGA' in key_data:
		print('in codon')