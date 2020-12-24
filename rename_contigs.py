#rename all contigs to make BRAKER happy

#imports
import os 
import csv

#directory 
in_dir = 'C:/Users/egann/Desktop/Aureococcus_strains/Final_assemblies/Genomes'

#get the files in the directory 
in_files = os.listdir(in_dir)

#for each file, open, rename the strain, and write to an out file 
for file in in_files:
	strain = file.split('_')[0]
	out_file = strain + '_assembly.fasta'
	#contig counter 
	
	in_dict = dict()
	key = ""
	with open(os.path.join(in_dir,file),'r') as f: 
		for line in f: 
			if line.startswith('>'):
				key = line.strip()
				in_dict[key] = ""
			else:
				in_dict[key] += line.strip()

	lengths_of_contigs = []

	for key in in_dict:
		lengths_of_contigs.append([key,len(in_dict[key])])

	lengths_of_contigs.sort(key=lambda x:int(x[1]), reverse=True)

	conversion = []

	count = 0

	for data in lengths_of_contigs:
		count = count + 1
		new_name = '>' + strain + '_' + str(count)
		conversion.append([data[0],new_name])

	out_file = strain + '_assembly.fasta'

	with open(os.path.join(in_dir,out_file),'w') as o:
		for key in in_dict:
			count = 0
			for data in conversion:
				if key == data[0]:
					count = count + 1
					o.write(data[1])
					o.write('\t')
			if count == 0:
				print('not good')
			o.write(in_dict[key])
			o.write('\n')

	conversion_out = strain + '_conversion.txt'

	with open(os.path.join(in_dir,conversion_out),'w') as o:
		writer = csv.writer(o,delimiter='\t')
		writer.writerows(conversion)