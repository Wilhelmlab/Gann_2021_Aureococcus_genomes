#pull out all proteins with the same information from the 
#table of interest 

#imports
import os 
import csv 

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/eggNOG/of interest'

#open file with lines of interest 
table_of_interest = []

with open(os.path.join(directory,'carbohydrate_degrading.txt'),'r') as f:
	for line in f:
		table_of_interest.append(line.strip().split('\t'))

#get full eggNOG out table 
eggNOG_table = []

with open(os.path.join(directory,'eggNOG_table.txt'),'r') as f:
	for line in f:
		eggNOG_table.append(line.strip().split('\t'))

#using the table of interest
#parse through eggNOG table 
#if table of interest line is in eggNOG line
#write to an outfile 
to_pull = []

with open('temp.txt','w') as o: 
	writer = csv.writer(o,delimiter='\t')

	for line_of_interest in table_of_interest:
		#make the line a string
		string_of_interest = '_'.join(line_of_interest[1:])
		#parse through each eggNOG line 
		for eggNOG_line in eggNOG_table:
			eggNOG_data = '_'.join(eggNOG_line[4:])
			if string_of_interest == eggNOG_data:
				#write to a temp out file 
				to_pull.append(eggNOG_line[0])
				eggNOG_line.insert(0,line_of_interest[0])
				writer.writerow(eggNOG_line)


#remove lines within temp file then delete temp 
with open(os.path.join(directory,'eggNOG_full_carb_deg.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')

#pull all of the proteins from the fasta file

#open the fasta file and make a dictionary 
in_dict = dict()
key = ""

with open(os.path.join(directory,'all_plus_ref.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			key = line.strip().split(' ')[0]
			in_dict[key] = ""
		else:
			in_dict[key] += line.strip()

#using to_pull pull out all sequences and write to an 
#outfile 

with open(os.path.join(directory,'pulled_proteins.fasta'),'w') as o:
	for data in to_pull:
		for key in in_dict:
			if key.strip('>') == data:
				o.write(key)
				o.write('\n')
				o.write(in_dict[key])
				o.write('\n')