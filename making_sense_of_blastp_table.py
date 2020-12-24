#pull out top hits from all v. all blast table based
#on organism searched again. Pull out hit, evalue, only
#if 30% of the protein was covered 

#imports
import os
import csv

#directory
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing Proteomes/blastp_all_analysis'

#strains
#the RefCCMP1984 proteins all start with XP_ so that will be used 
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','XP_']

#for each strain perform the same analysis 
for strain in strains: 
	#get all protein names from that strain to check against 
	query_names = []

	if strain != 'XP_':
		protein_file = strain + '_proteins.fasta'
		with open(os.path.join(directory,protein_file),'r') as f:
			for line in f:
				if line.startswith('>'):
					query_names.append(line.strip().split(' ')[0].strip('>'))

	if strain == 'XP_':
		protein_file = 'RefCCMP1984_proteins.fasta'
		with open(os.path.join(directory,protein_file),'r') as f:
			for line in f:
				if line.startswith('>'):
					query_names.append(line.strip().split(' ')[0].strip('>'))		

	#make a smaller table where you only pull out those lines
	#where the query is the strain 
	strain_table_full = []

	with open(os.path.join(directory,'all_v_all.txt'),'r') as f:
		for line in f:
			if line.strip().split('\t')[0].startswith(strain):
				strain_table_full.append(line.strip().split('\t'))

	#for each strain as the subject
	#make a smaller table, with only top hit
	#pulled write to an out list of lists
	for strain_subject in strains:
		#pull the proteins from the subject strain
		subject_dict = dict()
		key = ""

		if strain_subject != 'XP_':
			protein_file = strain_subject + '_proteins.fasta'
			with open(os.path.join(directory,protein_file),'r') as f:
				for line in f:
					if line.startswith('>'):
						key = line.strip().split(' ')[0].strip('>')
						subject_dict[key] = ""
					else:
						subject_dict[key] += line.strip()

		if strain_subject == 'XP_':
			protein_file = 'RefCCMP1984_proteins.fasta'
			with open(os.path.join(directory,protein_file),'r') as f:
				for line in f:
					if line.startswith('>'):
						key = line.strip().split(' ')[0].strip('>')
						subject_dict[key] = ""
					else:
						subject_dict[key] += line.strip()
		
		#make a smaller table from top hits
		strain_table_by_strain = []
		seen = set()


		for line in strain_table_full:
			if line[0] not in seen:
				
				if line[1].startswith(strain_subject):
					seen.add(line[0])
					strain_table_by_strain.append(line)

		#use the query proteins to see if a top hit exists
		#but only pull if length of alignment is >30 percent
		#the length of the 
		out_list_by_subject_strain = []

		for name in query_names:
			out_line_by_name = [name]
			#search smaller table for query name 
			present_count = 0
			for line in strain_table_by_strain:
				if name == line[0]:
					length_alignment = int(line[3])

					for subject in subject_dict:
						if subject == line[1]:
							if length_alignment/len(subject_dict[subject]) >= 0.3:
								out_line_by_name.append(line[1])
								out_line_by_name.append(line[10])
								present_count = present_count + 1
			if present_count == 0:
				out_line_by_name.append('-')
				out_line_by_name.append('-')
				

			out_list_by_subject_strain.append(out_line_by_name)




		if strain != 'XP_':
			if strain_subject != 'XP_':
				out_name = strain + '_' + strain_subject + '_best_hit.txt'
			else:
				out_name = strain + '_' + 'RefCCMP1984_best_hit.txt'
		if strain == 'XP_':
			if strain_subject != 'XP_':
				out_name = 'RefCCMP1984_' + strain_subject + '_best_hit.txt'
			else:
				out_name = 'refCCMP1984_RefCCMP1984_best_hit.txt'

		with open(os.path.join(directory,'temp.txt'),'w') as o:
			writer = csv.writer(o,delimiter='\t')
			for line in out_list_by_subject_strain:
				writer.writerow(line)

		with open(os.path.join(directory,out_name),'w') as o:

			with open(os.path.join(directory,'temp.txt'),'r') as f:
				for line in f:
					if line != '\n':
						o.write(line)

		os.remove(os.path.join(directory,'temp.txt'))