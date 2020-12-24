#split contigs into chunks of 10 Mb to be able to upload

#imports 
import os
from collections import OrderedDict

#directory
directory_path = 'C:/Users/egann/Desktop/Aureococcus_strains/Final_assemblies/split'
in_path = 'C:/Users/egann/Desktop/Aureococcus_strains/Final_assemblies'
#get all files 
in_files = os.listdir(in_path)

for file in in_files:
	if '_assembly.fasta' in file:
		new_name_1 = file.strip('.fasta') + '_chunk_1.fasta'
		new_name_2 = file.strip('.fasta') + '_chunk_2.fasta'
		new_name_3 = file.strip('.fasta') + '_chunk_3.fasta'
		new_name_4 = file.strip('.fasta') + '_chunk_4.fasta'
		new_name_5 = file.strip('.fasta') + '_chunk_5.fasta'
		new_name_6 = file.strip('.fasta') + '_chunk_6.fasta'
		new_name_7 = file.strip('.fasta') + '_chunk_7.fasta'
		new_name_8 = file.strip('.fasta') + '_chunk_8.fasta'
		new_name_9 = file.strip('.fasta') + '_chunk_9.fasta'

		o1 = open(os.path.join(directory_path,new_name_1),'w')
		o2 = open(os.path.join(directory_path,new_name_2),'w')
		o3 = open(os.path.join(directory_path,new_name_3),'w')
		o4 = open(os.path.join(directory_path,new_name_4),'w')
		o5 = open(os.path.join(directory_path,new_name_5),'w')
		o6 = open(os.path.join(directory_path,new_name_6),'w')
		o7 = open(os.path.join(directory_path,new_name_7),'w')
		o8 = open(os.path.join(directory_path,new_name_8),'w')
		o9 = open(os.path.join(directory_path,new_name_9),'w')

		#make dictionaries
		in_dict = OrderedDict()
		key = ""

		#open file 
		with open(os.path.join(in_path,file),'r') as f:
			for line in f:
				if line.startswith('>'):
					key = line.strip()
					in_dict[key] = ""
				else:
					in_dict[key] += line.strip()

		#split into out groups 
		count = 0

		for key in in_dict:
			count = count + len(in_dict[key])
			if count < 9000000:
				o1.write(key)
				o1.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o1.write(data)
					o1.write('\n')
			if 9000000 < count < 18000000:
				o2.write(key)
				o2.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o2.write(data)
					o2.write('\n')
			if 18000000 < count < 27000000:
				o3.write(key)
				o3.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o3.write(data)
					o3.write('\n')
			if 27000000 < count < 36000000:
				o4.write(key)
				o4.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o4.write(data)
					o4.write('\n')
			if 36000000 < count < 45000000:
				o5.write(key)
				o5.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o5.write(data)
					o5.write('\n')
			if 45000000 < count < 54000000:
				o6.write(key)
				o6.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o6.write(data)
					o6.write('\n')
			if 54000000 < count < 63000000:
				o7.write(key)
				o7.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o7.write(data)
					o7.write('\n')
			if 63000000 < count < 72000000:
				o8.write(key)
				o8.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o8.write(data)
					o8.write('\n')
			if  count > 72000000:
				o9.write(key)
				o9.write('\n')
				n = 80 # chunk length
				chunks = [in_dict[key][i:i+n] for i in range(0, len(in_dict[key]), n)]
				for data in chunks:
					o9.write(data)
					o9.write('\n')

		o1.close()
		o2.close()
		o3.close()
		o4.close()
		o5.close()
		o6.close()
		o7.close()
		o8.close()
		o9.close()