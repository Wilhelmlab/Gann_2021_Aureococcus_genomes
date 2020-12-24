##Pulling genes for concatination
##for phylogenetics 

#imports 
import os
import csv 

#directory of tsv files
directory_tsv = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Phylogenetics_concatanation/combined_tables'


#get all files in tsv directory 
tsv_files = os.listdir(directory_tsv)

busco_names = set()
by_strain = []

#get list of complete files 
for file in tsv_files:
	complete_by_strain = [file.strip('tsv')]

	#open file and make table
	tsv_table = []

	with open(os.path.join(directory_tsv,file),'r') as f:
		for line in f:
			if line.startswith('#') == False:
				tsv_table.append(line.strip().split('\t'))

	#search for complete busco terms 
	for line in tsv_table:
		if line[0] not in busco_names:
			busco_names.add(line[0])
		if line[1] == 'Complete':
			if float(line[3]) > 150:
				complete_by_strain.append(line[0])

	by_strain.append(complete_by_strain)

#figure out which busco names are found in all five
completeness_of_busco_names = []

for name in busco_names:
	by_name = [name]
	for strain in by_strain:
		if name in strain:
			by_name.append(strain[0])
	if len(by_name) == 7:
		completeness_of_busco_names.append(by_name)

print(len(completeness_of_busco_names))

#pull the name of the coding sequence for each of the 
#busco hit found in all 
sequences_to_use = []

for file in tsv_files:
	complete_by_strain = []

	#open file and make table
	tsv_table = []

	with open(os.path.join(directory_tsv,file),'r') as f:
		for line in f:
			if line.startswith('#') == False:
				tsv_table.append(line.strip().split('\t'))

	for line in tsv_table:
		for name in completeness_of_busco_names:
			if line[0] == name[0]:
				if line[1] == 'Complete': 
					to_add = line[2] + '-' + name[0]
					complete_by_strain.append(to_add)

	sequences_to_use.append(complete_by_strain)

#make a dictionary of all proteins 
protein_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Phylogenetics_concatanation'

in_dict  = dict()
key = ""

with open(os.path.join(protein_directory,'all_proteins.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			key = line.strip().split(' ')[0]
			in_dict[key] = ""
		else:
			in_dict[key] += line.strip()

seq_count = 0
out_dict = dict()

for data in sequences_to_use:
	seq_count = seq_count + 1
	name = '>' + data[0].split('-')[0]
	out_dict[name] = ""


	for info in data:
		for key in in_dict:
			if key.strip('>') == info.split('-')[0]:
				out_dict[name] += in_dict[key]

with open(os.path.join(protein_directory,'seqs_used.txt'),'w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(sequences_to_use)

#write to an out file 
with open(os.path.join(protein_directory,'concatinated_sequences.fasta'),'w') as o:
	for line in out_dict:
		o.write(line)
		o.write('\n')
		o.write(out_dict[line])
		o.write('\n')