#Date: 10.20.2020
###Get the number of each type of KEGG_KO_out 
###and put into a table, with each KO number as well 

#imports 
import os 
import csv
from collections import defaultdict

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/KEGG_ko_similarities'

#open presence absence file 
kegg_ko_table = []


with open(os.path.join(directory,'KEGG_ko_out.txt'),'r') as f: 
	for line in f: 
		kegg_ko_table.append(line.strip().split('\t'))

headers = kegg_ko_table[0]

del(kegg_ko_table[0])

#get all combinations of kegg table presences absence 
combinations = set()

for line in kegg_ko_table:
	if "".join(line[1:6]) not in combinations:
		combinations.add("".join(line[1:6]))

#make a default dic of kegg terms 
#with all combinations 

combo_dict = defaultdict(list)

for order in combinations:
	for line in kegg_ko_table:
		if "".join(line[1:6]) == order: 
			combo_dict[order].append(line[0])

#write this as an outformat that can then be used in 
#r to generate venn diagrma plot 
R_combinations = ['n12', 'n13', 'n14', 'n15', 'n23','n24','n25','n34','n35','n45','n123','124','n125','n134','n135','n145','n234','n235','n245','n345','n1234','n1235','n1245','n1345','n2345','n12345']

with open(os.path.join(directory,'pan_genome_venn_diagram_R_data.txt'),'w') as o:
	for r_name in R_combinations:
		need_zero = (list(r_name.strip('n')))
		r_name_count = 0

		for combo_name in combo_dict:
			combo_name_data = list(combo_name)

			correct_value_total = 0		

			for data in need_zero:

				if combo_name_data[int(data)-1] == '1':
					correct_value_total = correct_value_total + 1

			if correct_value_total == len(need_zero):
				r_name_count = r_name_count + len(combo_dict[combo_name])

		out_line = r_name + ' = ' + str(r_name_count) + ',\n'
		o.write(out_line)

	single = 0
	while single < 5:
		single_count = 0
		for combo_name in combo_dict:
			combo_name_data = list(combo_name)
			if combo_name_data[single] == '1':
				single_count = single_count + len(combo_dict[combo_name])
		out_line = 'area' + str(single) + ' = ' + str(single_count) + ',\n'
		o.write(out_line)
		single = single + 1

###pull out what percentage of each type is for each organism 
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984']

out_all_strains = []

##headers
headers = []

for combo_name in combo_dict:
	headers.append(combo_name)

headers.sort()

numbers = ['number of genomes']

for header in headers: 
	header_data = list(header)
	count = 0
	for data in header_data:
		count = count + int(data)
	numbers.append(count)

headers.insert(0,'Combination (P=1,A=0)')

single_strain = 0
while single_strain < 5:
	#make an outlist with the number and also 
	#the name 
	out_strain_list_of_list = []

	single_count = 0
	for combo_name in combo_dict:
		combo_name_data = list(combo_name)
		if combo_name_data[single_strain] == '1':
			out_strain_list_of_list.append([combo_name,len(combo_dict[combo_name])])
		else:
			out_strain_list_of_list.append([combo_name,'not in'])
	
	#order the list of lists 
	out_strain_list_of_list = sorted(out_strain_list_of_list, key=lambda x: x[0])
	
	#write out just the data 
	out_data = [strains[single_strain]]

	for lis in out_strain_list_of_list:
		out_data.append(lis[1])

	out_all_strains.append(out_data)
	single_strain = single_strain + 1

#add in the headers
out_all_strains.insert(0,headers)
out_all_strains.insert(0,numbers)

#write to an out file 
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(zip(*out_all_strains))

with open(os.path.join(directory,'all_ko_combinations_by_strain.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)
