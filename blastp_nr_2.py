#assign to domain from top hit 
#using inputs from blastp_nr.py

#imports
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/blast_against_nr'

#get all organism_nr data
#which gives domain 

organisms_data = []

with open(os.path.join(directory,'organisms_nr.txt'),'r') as f:
	for line in f:
		organisms_data.append(line.strip().split('\t'))


#append all_nr_data file with domain 
nr_data_table = []

with open(os.path.join(directory,'all_nr_data.txt'),'r') as f:
	for line in f: 
		to_add = line.strip().split('\t')

		for info in organisms_data:
			query = '[' + info[0] + ']'
			if query in to_add[2]:
				to_add.append(info[1])

		if len(to_add) == 3:
			to_add.append('N')

		nr_data_table.append(to_add)

#write nr_data_table to file 

with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(nr_data_table)

with open(os.path.join(directory,'all_nr_data_plus_domain.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')


#get domains
domains = set()

for line in nr_data_table:
	if line[3] not in domains:
		domains.add(line[3])

#print data 
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984']

for strain in strains:
	strain_table = []
	for line in nr_data_table:
		if line[0].startswith(strain):
			strain_table.append(line[3])
	print(strain)
	print(len(strain_table))
	for domain in domains:
		print(domain)
		print(strain_table.count(domain))

	print('\n')