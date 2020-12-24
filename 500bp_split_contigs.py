#Outcome: This script takes contigs and splits them into 500 bp chunks
#to then be able to fed through Kaiju 

#imports
import os 

#location of working directory
#this will change 
directory_path = "C:/Users/WilhelmLab/Desktop/ERG - computer backup/Aa_strains"
out_path = "C:/Users/WilhelmLab/Desktop/ERG - computer backup/out"
#get list of .fa files (from Redundans.py) in directory 
directory_files = os.listdir(directory_path)

#open each file, make a dictonary for each fasta header, and split
#into 500bp, while renaming the fasta headers

for file in directory_files:
	in_dict = dict()
	key = ""
	#get the strain for that file
	strain = '>' + file.strip('_contigs_reduced.fasta')
	#open the file from the directory
	with open(os.path.join(directory_path,file), 'r') as f: 
		#make a dictionary with the key being the fasta header
		#modified so it has the strain name added to the front
		for line in f:
			if line.startswith('>'):
				line_name = line.strip().replace('_pilon','').replace('>','')
				key = strain + '_' + line_name
				in_dict[key] = ''
			else: 
				in_dict[key] += line.strip()
	#split the sequence into 500 bp sizes and write to an out dict
	out_file = strain.strip('>') + '_500bp_substrings.fasta'
	with open(os.path.join(out_path, out_file), 'w') as o:
		for key in in_dict:
			n = 500
			substring_list = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
			#write substring data to a new out file with the 
			#position in the list being appended to the key
			list_count = 1 
			for data in substring_list:
				new_name = key + '_' + str(list_count)
				o.write(new_name)
				o.write('\n')
				o.write(data)
				o.write('\n')
				print(new_name)
				print(data)
				list_count = list_count + 1