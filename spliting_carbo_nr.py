#pull out all proteins with the same information from the 
#table of interest 

#imports
import os 
import csv 

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/nitrogen metabolism enzymes'

#open modified eggNOG table 
eggNOG_table = []
#get the categories
seen_categories = set()

with open(os.path.join(directory,'eggNOG_full_nitrogen_met.txt'),'r') as f:
	for line in f:
		eggNOG_table.append(line.strip().split('\t'))
		if line.strip().split('\t')[0] not in seen_categories:
			seen_categories.add(line.strip().split('\t')[0])

#open nr blast table and only add top hit
blast_table_nr = []

with open(os.path.join(directory,'nitrogen_nr.txt'),'r') as f:
	for line in f:
		blast_table_nr.append(line.strip().split('\t'))

#for each category, split and write to new files 
for category in seen_categories:
	#make a new out file 
	if category == 'choline/ethanolamine':
		out = 'choline_ethanolamine_bt_split.txt'
	else:
		out = category + '_bt_split.txt'
	#write to a temp file first 
	with open('temp.txt','w') as o:
		writer = csv.writer(o,delimiter='\t')
		#open the blast table, search for eggNOG category
		#if it is in that category, write to temp file 
		for bt_line in blast_table_nr:
			for eN_line in eggNOG_table:
				if bt_line[0] == eN_line[1]:
					if eN_line[0] == category:
						writer.writerow(bt_line)
	#write to final file 
	with open(os.path.join(directory,out),'w') as o:
		with open('temp.txt','r') as f:
			for line in f: 
				if line != '\n':
					o.write(line)