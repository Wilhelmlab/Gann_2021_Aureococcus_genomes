#Pull out the selenoproteins top hits from

#imports 
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Selenoproteins'

#get all queries from fasta file 
fasta_headers = []

with open(os.path.join(directory,'Aureococcus_selenoproteins.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			fasta_headers.append(line.strip().strip('>'))

for x in fasta_headers:
	print(x)

strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984']

#get blast table 
blast_table = []

with open(os.path.join(directory,'Seleno_all_plus.txt'),'r') as f:
	for line in f:
		blast_table.append(line.strip().split('\t'))

out = []

for strain in strains: 
	out_list = [strain]

	strain_table = []
	for line in blast_table:
		if line[1].startswith(strain):
			strain_table.append(line)
	
	
	for header in fasta_headers:
		count = 0
		for line in strain_table:
			if header.startswith(line[0]):
				count = count + 1

		if count == 0:
			out_list.append('0')
		else:
			out_list.append('1')

	out.append(out_list)

headers = ['header']

for header in fasta_headers:
	headers.append(str(header.strip('Aa_').split('_')[1:]))

out.insert(0,headers)

with open(os.path.join(directory,'temp.txt'),'w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(zip(*out))

with open(os.path.join(directory,'ref1984_selenos_by_strain_PA.txt'),'w') as o:
	with open(os.path.join(directory,'temp.txt'),'r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove(os.path.join(directory,'temp.txt'))