#this script pulls top evalue from each contig or says whether there is not 
#a blastn hit to the reference genome CCMP1984

#imports
import os
import csv 

#get directories
blastn_table_directory = 'C:/Users/WilhelmLab/Desktop/ERG - computer backup/blastn_tables'
contig_directory = 'C:/Users/WilhelmLab/Desktop/ERG - computer backup/Aa_strains'

#get list of contig files
contig_files = os.listdir(contig_directory)
blastn_files = os.listdir(blastn_table_directory)

#aureococcus strains list to open correct files
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984']

#for each strain, get the name of each contig from the contig file

for strain in strains: 
	contig_names = []
	#open contig file add contig names, with > to contig_names
	for file in contig_files:
		if file.startswith(strain):
			with open(os.path.join(contig_directory,file),'r') as f:
				for line in f:
					if line.startswith('>'):
						contig_names.append(line.strip().strip('>'))
						
	#look for contig name in blastn file and pull blastn table
	blastn_table_for_strain = []
	
	for file in blastn_files:
		if file.startswith(strain):
			with open(os.path.join(blastn_table_directory,file),'r') as f:
				for line in f:
					blastn_table_for_strain.append(line.strip().split('\t'))
					
	#get the top from each strain 
	blastn_top_hit = []
	already_seen = set()
	
	for line in blastn_table_for_strain:
		if line[0] not in already_seen:
			already_seen.add(line[0])
			blastn_top_hit.append(line)

	#for each contig, pull out the subject name, and evalue from the 
	#condensed blast table 
	out_blastn_hit_evalue = []
	
	for contig in contig_names:
		#use count == 0 to indicate no hit
		count = 0
		for line in blastn_top_hit:
			if contig == line[0]:
				count = count + 1
				out_blastn_hit_evalue.append([contig,line[1],line[10]])
		if count == 0:
			out_blastn_hit_evalue.append([contig,'none','none'])
			
	#write to an out file
	
	#use the strain name to generate a new name
	out_name = strain + '_blastn_hit_evalue.txt'
	
	with open(out_name,'w') as o:
		writer = csv.writer(o,delimiter='\t')
		writer.writerows(out_blastn_hit_evalue)