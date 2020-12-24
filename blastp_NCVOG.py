#pull proteins that alignments are at least 
#30% the length of the query and the subject 
#and with an evalue < 1e-10

#imports
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/blastp against NCVOGs'

#open blastp table 
#pull top hit for each protein 
smaller_blastp_table = []
seen = set()

with open(os.path.join(directory,'NCVOG_all.txt'),'r') as f:
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

NCVOG_sequences = dict()
key = ""

with open(os.path.join(directory,'NCVOG.fa'),'r') as f:
	for line in f:
		if line.startswith('>'):
			key = line.strip()
			NCVOG_sequences[key.strip('>')] = ""
		else:
			NCVOG_sequences[key.strip('>')] += line.strip()


#for each protein in strain sequences, pull out
#top hit, evalue, only if 30% of both the subject and query 
#are the alignment 

out = []
for sequence in strain_sequences:
	out_line = [sequence]
	len_seq = len(strain_sequences[sequence])
	#find line in table 
	for line in smaller_blastp_table:
		if line[0] == sequence:
			
			for data in NCVOG_sequences:
				sub = '|' + line[1] +'|'
				if sub in data:
					NCVOG_len = len(NCVOG_sequences[data])
					if int(line[3]) > 0.3*NCVOG_len:
						if int(line[3]) > 0.3*len_seq:
							out_line.append(line[1])
							out_line.append(line[10])
	if len(out_line) == 1:
		out_line.append('-')
		out_line.append('-')

	out.append(out_line)


#write to an outfile 
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(out)

with open(os.path.join(directory,'viral_protein_hits.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')