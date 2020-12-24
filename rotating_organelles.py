##Rotates the chloroplasts and Mitochondria so the circular 
##chromosome begins at the 16S on the plus strand using
##the gff annotations from Kbase 

#script path: C:/Users/egann/Desktop/Aureococcus_strains/scripts/rotating_organelles.py

#imports
import os 
import csv 
from Bio.Seq import Seq

#definitions
def my_reverse_complement(seq):
    return Seq(seq).reverse_complement()

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Organelles/rotating_plastids'

#open organelles fasta and write to a dictionary 
fasta_dict = dict()
key = ""

with open(os.path.join(directory,'starting.fasta'),'r') as f: 
	for line in f:
		if line.startswith('>'):
			key = line.strip()
			fasta_dict[key] = ""
		else:
			fasta_dict[key] += line.strip()


#open .gff file and write to a table only those that have 16S in the 8th column
gff_table = []

with open(os.path.join(directory,'starting.gff'),'r') as f: 
	for line in f:
		if len(line.strip().split('\t')) == 9:
			if '16S' in line.strip().split('\t')[8]:
				gff_table.append(line.strip().split('\t'))


#get the 16S on the same strand by generating the REVCOMP where the 16S is on the 
#opposite strand 
same_strand_dict = dict()
key = ""

for line in gff_table:
	for key in fasta_dict:
		if line[0].startswith(key.strip('>')):
			if line[6] == '-':
				same_strand_dict[key] = str(my_reverse_complement(fasta_dict[key]))
			if line[6] == '+':
				same_strand_dict[key] = fasta_dict[key]

#write same strand dict to an out file 
with open(os.path.join(directory,'16S_on_same_strand.fasta'),'w') as o:
	for key in same_strand_dict:
		o.write(key)
		o.write('\n')
		o.write(same_strand_dict[key])
		o.write('\n')

#open the Kbase .gff generated for those on the same strand using the same_strand_dict output 
same_strand_gff_table = []

with open(os.path.join(directory,'same_strand.gff'),'r') as f: 
	for line in f:
		if len(line.strip().split('\t')) == 9:
			if '16S' in line.strip().split('\t')[8]:
				same_strand_gff_table.append(line.strip().split('\t'))


#reorder contigs to start at 16S position
same_strand_starting_16S_dict = dict()

for line in same_strand_gff_table:
	for key in same_strand_dict:
		if key.strip('>') == line[0]:
			start = int(line[3]) - 1
			new_sequence = same_strand_dict[key][start:] + same_strand_dict[key][:start]
			same_strand_starting_16S_dict[key] = new_sequence


#write to an out file 
with open(os.path.join(directory,'plus_strand_starting_with_16S.fasta'),'w') as o:
	for key in same_strand_starting_16S_dict:
		o.write(key)
		o.write('\n')
		o.write(same_strand_starting_16S_dict[key])
		o.write('\n')


#open organelles fasta and write to a dictionary 
fasta_dict = dict()
key = ""

with open(os.path.join(directory,'reference_plastids.fasta'),'r') as f: 
	for line in f:
		if line.startswith('>'):
			key = line.strip()
			fasta_dict[key] = ""
		else:
			fasta_dict[key] += line.strip()


#open .gff file and write to a table only those that have 16S in the 8th column
gff_table = []

with open(os.path.join(directory,'reference_plastids.gff'),'r') as f: 
	for line in f:
		if len(line.strip().split('\t')) == 9:
			if '16S' in line.strip().split('\t')[8]:
				gff_table.append(line.strip().split('\t'))


#reorder contigs to start at 16S position
same_strand_starting_16S_dict = dict()

for line in gff_table:
	for key in fasta_dict:
		if key.strip('>') == line[0]:
			start = int(line[3]) - 1
			new_sequence = fasta_dict[key][start:] + fasta_dict[key][:start]
			same_strand_starting_16S_dict[key] = new_sequence


#write to an out file 
with open(os.path.join(directory,'ref_starting_with_16S.fasta'),'w') as o:
	for key in same_strand_starting_16S_dict:
		o.write(key)
		o.write('\n')
		o.write(same_strand_starting_16S_dict[key])
		o.write('\n')
