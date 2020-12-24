#Get the length, GC content of each contig in a file 

#imports
import os
import csv 

#directory paths
in_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/polished_redundancies_removed'
out_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/removing_bacterial_contaimination/GC_content_results'

#get all sequence file in in_directory 
directory_files = os.listdir(in_directory)

#open each file
#make a dictionary where the term is the fasta header 
#determine length and number of Gs Cs and percentage of GC in a contig
#write to an out list 

for file in directory_files:

	#get the file name to then change for out file name
	file_name = file.split('.')[0]
	out_file_name = file_name + '_GC_and_length.txt'

	#make a dictionary for the fasta sequences 
	fasta_dict = dict()
	key = ""

	with open(os.path.join(in_directory,file),'r') as f:
		for line in f:
			if line.startswith('>'):
				key = line.strip()
				fasta_dict[key] = ""
			else:
				fasta_dict[key] += line.strip()

	#for each contig determine length, and GC content
	out_list = []

	for contig in fasta_dict:
		length = len(fasta_dict[contig])
		G_C_count = fasta_dict[contig].count('G')+fasta_dict[contig].count('C')
		Percent_GC = float(G_C_count / length)
		out_list.append([contig,length,Percent_GC])

	#write to an out file
	with open(os.path.join(out_directory,out_file_name),'w') as o:
		writer = csv.writer(o,delimiter='\t')
		writer.writerows(out_list)
		