#this program pulls together the rest of the outputs from determining which
#contigs are bacterial contamination

#imports
import os
import csv 

#file directories 
contig_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/polished_redundancies_removed'
kaiju_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/removing_bacterial_contaimination/Kaiju_results/Kaiju_classification_files'
blastn_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/removing_bacterial_contaimination/blastn_results/blastn_hit_evalue_tables'
GC_content_length_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/removing_bacterial_contaimination/GC_content_results'

#get files within each directory 
contig_files = os.listdir(contig_directory)
kaiju_files = os.listdir(kaiju_directory)
blastn_files = os.listdir(blastn_directory)
GC_content_length_files = os.listdir(GC_content_length_directory)

#name the strains to use to then parse all information for 
strains = ['CCMP1984','CCMP1850','CCMP1794','CCMP1707']

#for each strain pull all data from each directory output file from previous scripts 
for strain in strains:
	#get names of all contigs 
	contig_names = []

	for file in contig_files:
		if file.startswith(strain):
			with open(os.path.join(contig_directory,file),'r') as f:
				for line in f:
					if line.startswith('>'):
						contig_names.append(line.strip().strip('>'))

	#make lists of all data from three outputs
	kaiju_table = []
	blastn_table = []
	GC_length_table = []

	for file in kaiju_files:
		if file.startswith(strain):
			with open(os.path.join(kaiju_directory,file),'r') as f:
				for line in f:
					kaiju_table.append(line.strip().split('\t'))

	for file in blastn_files:
		if file.startswith(strain):
			with open(os.path.join(blastn_directory,file),'r') as f:
				for line in f:
					blastn_table.append(line.strip().split('\t'))

	for file in GC_content_length_files:
		if file.startswith(strain):
			with open(os.path.join(GC_content_length_directory,file),'r') as f:
				for line in f:
					GC_length_table.append(line.strip().split('\t'))

	#pull all data for each contig
	out_list = []

	for contig in contig_names:
		by_contig = [contig]

		count = 0
		for line in GC_length_table:
			
			if line[0] == contig:
				by_contig.append(line[1])
				by_contig.append(line[2])
				count = count + 1
		if count == 0:
			by_contig.append('-')

		count = 0
		for line in kaiju_table:
			
			if line[0] == contig:
				by_contig.append(line[2])
				count = count + 1
		if count == 0:
			by_contig.append('-')

		count = 0
		for line in blastn_table:
			
			if line[0] == contig:
				by_contig.append(line[2])
				count = count + 1
		if count == 0:
			by_contig.append('-')

		out_list.append(by_contig)

	#write to an outfile 

	out_name = strain + '_compiled_data.txt'

	with open(out_name,'w') as o:
		writer = csv.writer(o,delimiter='\t')
		writer.writerows(out_list)
