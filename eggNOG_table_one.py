#this script allows for the pulling of different overall
#information from the eggNOG output table 

#imports 
import os 
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/eggNOG'

#strains so each can be separated
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','XP_']

#make a list of all GO_terms (line[6]), KEGG_KO (line[8]),
#KEGG_pathways (line[9]), BRITE (line[13]), description (line[21])
GO_terms = set()
KEGG_ko = set()
KEGG_pathways = set()
BRITE_names = set()
Descriptions = set() 

with open(os.path.join(directory,'eggNOG_table.txt'),'r') as f:
	for line in f: 
		line_data = line.strip('\n').split('\t')

		#split gene ontologies by , and add them 
		#to GO_terms 
		if len(line_data[6]) != 0:
			GO_info = line_data[6].split(',')
			for info in GO_info:
				if info not in GO_terms:
					GO_terms.add(info)
		#split KEGG ko by , and remove ko:
		if len(line_data[8]) != 0:
			KEGG_ko_info = line_data[8].split(',')
			for info in KEGG_ko_info:
				if info.strip('ko:') not in KEGG_ko:
					KEGG_ko.add(info.strip('ko:'))
		#split KEGG_pathways by , and add to KEGG_pathways
		if len(line_data[9]) != 0:
			KEGG_pathways_info = line_data[9].split(',')
			for info in KEGG_pathways_info:
				if info not in KEGG_pathways:
					KEGG_pathways.add(info)
		#split BRITE names by , and add to BRITE_names
		if len(line_data[13]) != 0:
			BRITE_info = line_data[13].split(',')
			for info in BRITE_info:
				if info not in BRITE_names:
					BRITE_names.add(info)
		#add descriptions to description list
		if len(line_data) == 22:
			if line_data[21] not in Descriptions:
				Descriptions.add(line_data[21])


#out list of lists
out_GO_terms = [GO_terms]
out_KEGG_ko = [KEGG_ko]
out_KEGG_pathways = [KEGG_pathways]
out_BRITE_names = [BRITE_names]
out_Descriptions = [Descriptions]


#for each strain pull out the data of interest from the 
#eggNOG_table 
for strain in strains: 
	#open the eggNOG table, and add the line to the 
	#strain eggNOG table if line[0] starts with the strain 
	strain_table = []
	strain_GO_terms = set()
	strain_KEGG_ko = set()
	strain_KEGG_pathways = set()
	strain_BRITE_names = set()
	strain_Descriptions = set() 

	with open(os.path.join(directory,'eggNOG_table.txt'),'r') as f:
		for line in f: 
			if line.strip().split('\t')[0].startswith(strain):
				strain_table.append(line)

	for line in strain_table: 
		line_data = line.strip('\n').split('\t')

		#split gene ontologies by , and add them 
		#to GO_terms 
		if len(line_data[6]) != 0:
			strain_GO_info = line_data[6].split(',')
			for info in strain_GO_info:
				if info not in strain_GO_terms:
					strain_GO_terms.add(info)
		#split KEGG ko by , and remove ko:
		if len(line_data[8]) != 0:
			strain_KEGG_ko_info = line_data[8].split(',')
			for info in strain_KEGG_ko_info:
				if info.strip('ko:') not in strain_KEGG_ko:
					strain_KEGG_ko.add(info.strip('ko:'))
		#split KEGG_pathways by , and add to KEGG_pathways
		if len(line_data[9]) != 0:
			strain_KEGG_pathways_info = line_data[9].split(',')
			for info in strain_KEGG_pathways_info:
				if info not in strain_KEGG_pathways:
					strain_KEGG_pathways.add(info)
		#split BRITE names by , and add to BRITE_names
		if len(line_data[13]) != 0:
			strain_BRITE_info = line_data[13].split(',')
			for info in strain_BRITE_info:
				if info not in strain_BRITE_names:
					strain_BRITE_names.add(info)
		#add descriptions to description list
		if len(line_data) == 22:
			if line_data[21] not in strain_Descriptions:
				strain_Descriptions.add(line_data[21])

	#search each respective term is in the 
	#subset from each strain 
	strain_out_GO_terms = []
	strain_out_KEGG_ko = []
	strain_out_KEGG_pathways = []
	strain_out_BRITE_names = []
	strain_out_Descriptions = []


	#Go_terms 
	for term in GO_terms:
		if term in strain_GO_terms:
			strain_out_GO_terms.append(1)
		else:
			strain_out_GO_terms.append(0)

	out_GO_terms.append(strain_out_GO_terms)

	#KEGG_ko
	for term in KEGG_ko:
		if term in strain_KEGG_ko:
			strain_out_KEGG_ko.append(1)
		else:
			strain_out_KEGG_ko.append(0)

	out_KEGG_ko.append(strain_out_KEGG_ko)

	#KEGG_pathway
	for term in KEGG_pathways:
		if term in strain_KEGG_pathways:
			strain_out_KEGG_pathways.append(1)
		else:
			strain_out_KEGG_pathways.append(0)

	out_KEGG_pathways.append(strain_out_KEGG_pathways)

	#BRITE
	for term in BRITE_names:
		if term in strain_BRITE_names:
			strain_out_BRITE_names.append(1)
		else:
			strain_out_BRITE_names.append(0)

	out_BRITE_names.append(strain_out_BRITE_names)

	#Descriptions
	for term in Descriptions:
		if term in strain_Descriptions:
			strain_out_Descriptions.append(1)
		else:
			strain_out_Descriptions.append(0)

	out_Descriptions.append(strain_out_Descriptions)


#zip lists to make it by row instead of by column
out_GO_terms = zip(*out_GO_terms)
out_KEGG_ko = zip(*out_KEGG_ko)
out_KEGG_pathways = zip(*out_KEGG_pathways)
out_BRITE_names = zip(*out_BRITE_names)
out_Descriptions = zip(*out_Descriptions)


#write to an out file for each 
#but for each row summing the four columns

#out_GO_terms 
#write to a temp
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	headers = ['term','CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984','total']
	writer.writerow(headers)
	for group in out_GO_terms:
		out_line = list(group)
		out_line.append(sum(out_line[1:]))

		writer.writerow(out_line)

#clean up 
with open(os.path.join(directory,'GO_terms_out.txt'),'w') as o:

	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')


#out_KEGG_ko 
#write to a temp
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	headers = ['term','CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984','total']
	writer.writerow(headers)
	for group in out_KEGG_ko:
		out_line = list(group)
		out_line.append(sum(out_line[1:]))

		writer.writerow(out_line)

#clean up 
with open(os.path.join(directory,'KEGG_ko_out.txt'),'w') as o:

	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')



#out_KEGG_pathways 
#write to a temp
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	headers = ['term','CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984','total']
	writer.writerow(headers)
	for group in out_KEGG_pathways:
		out_line = list(group)
		out_line.append(sum(out_line[1:]))

		writer.writerow(out_line)

#clean up 
with open(os.path.join(directory,'KEGG_pathways_out.txt'),'w') as o:

	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')


#out_Descriptions 
#write to a temp
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	headers = ['term','CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984','total']
	writer.writerow(headers)
	for group in out_Descriptions:
		out_line = list(group)
		out_line.append(sum(out_line[1:]))

		writer.writerow(out_line)

#clean up 
with open(os.path.join(directory,'Descriptions_out.txt'),'w') as o:

	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')


#out_BRITE_names 
#write to a temp
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	headers = ['term','CCMP1707','CCMP1794','CCMP1850','CCMP1984','ref1984','total']
	writer.writerow(headers)
	for group in out_BRITE_names:
		out_line = list(group)
		out_line.append(sum(out_line[1:]))

		writer.writerow(out_line)

#clean up 
with open(os.path.join(directory,'BRITE_names_out.txt'),'w') as o:

	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')