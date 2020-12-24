#pull final contig list

#imports
import os

#name the strains to use to then parse all information for 
strains = ['CCMP1984','CCMP1850','CCMP1794','CCMP1707']


#directories
contig_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/MinION Assemblies/polished_redundancies_removed'
to_pull_directory = 'C:/Users/egann/Desktop/Aureococcus_strains/MinION Assemblies/removing_bacterial_contaimination/compiled_results/final_list_of_contigs'

#files 
contig_files = os.listdir(contig_directory)
to_pull_files = os.listdir(to_pull_directory)

#for each strain pull all data from each directory output file from previous scripts 
for strain in strains:

	#pull contigs to pull
	to_pull = []

	for file in to_pull_files:
		if file.startswith(strain):
			with open(os.path.join(to_pull_directory,file),'r') as f:
				for line in f:
					headers = '>' + line.strip()
					to_pull.append(headers)

	print(len(to_pull))

	#pull contigs 
	in_dict = dict()
	key = ""

	for file in contig_files:
		if file.startswith(strain):
			with open(os.path.join(contig_directory,file),'r') as f:
				for line in f:
					if line.startswith('>'):
						key = line.strip()
						in_dict[key] = ""
					else:
						in_dict[key] += line.strip()


	out_file = strain + '_final_contigs.fasta'
	count = 0
	with open(out_file,'w') as o:
		for key in in_dict:
			for header in to_pull:
				if header == key:
					count = count + 1
					o.write(key)
					o.write('\n')
					o.write(in_dict[key])
					o.write('\n')

	print(count)
