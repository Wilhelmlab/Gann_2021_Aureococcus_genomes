#pull proteins that alignments are at least 
#30% the length of the query and the subject 
#and with an evalue < 1e-10

#imports
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/blast_against_nr'

#open blastp table 
#pull top hit for each protein 
smaller_blastp_table = []
seen = set()

with open(os.path.join(directory,'all_nr.txt'),'r') as f:
	for line in f:
		if line.strip().split('\t')[0] not in seen:
			seen.add(line.strip().split('\t')[0])
			smaller_blastp_table.append(line.strip().split('\t'))

#get NCVOG sequences and all strain sequences 
#and write both to a dictionary 
strain_sequences = dict()
key = ""

with open(os.path.join(directory,'all_plus_ref.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			key = line.strip().split(' ')[0]
			strain_sequences[key.strip('>')] = ""
		else:
			strain_sequences[key.strip('>')] += line.strip()

#for each protein in strain sequences, pull out
#top hit, evalue, only if 30% of both the subject and query 
#are the alignment 
organisms = set()

with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	for sequence in strain_sequences:
		out_line = [sequence]
		len_seq = len(strain_sequences[sequence])
		#find line in table 
		for line in smaller_blastp_table:
			if line[0] == sequence:
				if line[12].split('[')[1].strip(']') not in seen:
					organisms.add(line[12].split('[')[1].strip(']'))
				out_line.append(line[1])
				out_line.append(line[12])
		if len(out_line) == 1:
			out_line.append('-')
			out_line.append('-')
		writer.writerow(out_line)

with open(os.path.join(directory,'all_nr_data.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)
with open(os.path.join(directory,'organisms_nr.txt'),'w') as o:
	for line in organisms:
		o.write(line)
		o.write('\n')

os.remove('temp.txt')