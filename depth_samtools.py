#count the number of zero's present in samtools depth 
#files 

#imports
import os 
import csv

#directory 
directory = 'C:/Users/egann/Desktop/out'

#get files 
in_files = os.listdir(directory)

#for each file
#print the file name, the number of zeros in line[2]
#and the total 

for file in in_files:
	#print the file
	print(file)
	#open the file 
	zero_count = 0
	line_count = 0
	with open(os.path.join(directory,file),'r') as f:
		for line in f:
			line_count = line_count + 1
			if int(line.strip().split('\t')[2]) == 0:
				zero_count = zero_count + 1
	print(line_count)
	print(zero_count)