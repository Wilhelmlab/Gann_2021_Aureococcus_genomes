#Pull out the selenoproteins top hits from

#imports 
import os
import csv
from Bio.Seq import Seq

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Selenoproteins'

#get all subjects from fasta file 
fasta_dict = dict()
key = ""

with open(os.path.join(directory, 'Selenoprotein_hit_chunk_final.fasta'),'r') as f: 
	for line in f: 
		if line.startswith('>'):
			key = line.strip().split(' ')[0]
			fasta_dict[key] = ""
		else:
			fasta_dict[key] += line.strip()

strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984']

with open(os.path.join(directory,'temp.txt'),'w') as o:
	writer = csv.writer(o,delimiter='\t')
	for strain in strains:
		#make a dict for each strain 
		strain_dict = dict()
		key = ""

		in_file = strain + '_assembly.fasta'
		with open(os.path.join(directory,in_file),'r') as f:
			for line in f:
				if line.startswith('>'):
					key = line.strip()
					strain_dict[key] = ""
				else:
					strain_dict[key] += line.strip()

		#for each seq find in dictionary
		for term in fasta_dict:
			if term.startswith('>' + strain):
				if '_-_' in term:
					for key in strain_dict:
						if term.split('_-_')[0] == key:
							
							seq = Seq(fasta_dict[term])
							revcom_seq = seq.reverse_complement()
							start = strain_dict[key].find(str(revcom_seq))
							end = start + len(term)
							secis = [key,'secis element','-',term.split('_-_')[1].split('_')[0],term.split('_-_')[1].split('_')[1]]
							writer.writerow(secis)
							out = [key,term.strip('>'),'-',start,end]
							writer.writerow(out)

				if '_+_' in term:
					for key in strain_dict:
						if term.split('_+_')[0] == key:

							start = strain_dict[key].find(fasta_dict[term])
							end = start + len(term)
							out = [key,term.strip('>'),'+',start,end]
							writer.writerow(out)
							secis = [key,'secis element','+',term.split('_+_')[1].split('_')[0],term.split('_+_')[1].split('_')[1]]
							writer.writerow(secis)


with open(os.path.join(directory,'selenoprotein_gff_table.txt'),'w') as o:
	with open(os.path.join(directory,'temp.txt'),'r') as f:
		for line in f:
			if line != '\n':
				o.write(line)


os.remove(os.path.join(directory,'temp.txt'))