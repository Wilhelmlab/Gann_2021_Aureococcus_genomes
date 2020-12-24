##take all individual read mapping files and combine them 
##to make them easier to look at 

#location C:/Users/egann/Desktop/Aureococcus_strains/scripts/reworking_read_mapping_files.py

#imports 
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/read_mappings_QB2016/Individual_read_mappings'

#get all files from the directory 
files = os.listdir(directory)

#strains
strains = ['all_CDS','CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984']


#for each strain, add each number of reads mapped to a single out file 
for strain in strains: 
	print(strain)
	out_list = []

	for file in files:
		per_row = []
		if file.startswith(strain):
			with open(os.path.join(directory,file),'r') as f:
				for line in f:
					per_row.append(line.strip().split('\t'))

		for x in per_row:
			print(len(x))

	#write to a temp file then write to the actual out file 
#	with open('temp.txt','w') as o:
#		writer = csv.writer(o,delimiter='\t')
#		writer.writerows(zip(*out_list))

#	out_name = strain + '_combined_read_mappings.txt'

#	with open(os.path.join(directory,out_name),'w') as o:
#		with open('temp.txt','r') as f:
#			for line in f:
#				if line != '\t':
#					o.write(line)

#	os.remove('temp.txt')