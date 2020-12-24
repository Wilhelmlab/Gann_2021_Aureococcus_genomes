#pull out all proteins with the same information from the 
#table of interest 

#imports
import os 
import csv 

#directory 
directory = 'C:/Users/egann/Desktop'

#open file with lines of interest 
table_of_interest = []

with open(os.path.join(directory,'transporters_eggNOG.txt'),'r') as f:
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
		string_of_interest = '_'.join(line_of_interest)
		#parse through each eggNOG line 
		for eggNOG_line in eggNOG_table:
			eggNOG_data = '_'.join(eggNOG_line[4:])

			if string_of_interest == eggNOG_data:

				#write to a temp out file 
				to_pull.append(eggNOG_line[0])
				writer.writerow(eggNOG_line)


#remove lines within temp file then delete temp 
with open(os.path.join(directory,'eggNOG_transporters.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')