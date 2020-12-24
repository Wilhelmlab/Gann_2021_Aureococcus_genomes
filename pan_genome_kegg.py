#this script takes the kegg data and separates it
#by number of genomes it is present in 

#imports
import os 
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/KEGG_ko_similarities_pan_genome'

#get all the KEGG ko data
ko_data = []

with open(os.path.join(directory,'ko_data.txt'),'r') as f:
	for line in f:
		ko_data.append(line.strip().split('\t'))

#get all the genomic information
found_in_genomes = []

with open(os.path.join(directory,'KEGG_ko_out.txt'),'r') as f: 
	for line in f:
		found_in_genomes.append(line.strip().split('\t'))

del found_in_genomes[0]

#combine tables using kegg ko number to do it 
combined_table = []

for ko_data_line in ko_data:
		out_line = ko_data_line
		for genome_data in found_in_genomes:
				if ko_data_line[0] == genome_data[0]:
					genomes = "'" + "".join(genome_data[1:6])
					out_line.append(genomes)
					out_line.append(genome_data[6])
		combined_table.append(out_line)
#write to a temp file and then the actual out file 
with open('temp.txt','w') as o: 
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(combined_table)

with open(os.path.join(directory,'KEGG_data_with_genome_info.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)