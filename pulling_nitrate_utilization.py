##pull coding sequences pertaining to nitrate utilization 
##and separate by type

#imports
from __future__ import division
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/read_mappings_QB2016/nitrogen_utlization'

#make a read mappings table 
rm_table = []

with open(os.path.join(directory,'all_CDS_read_mappings.txt'),'r') as f:
	for line in f:
		rm_table.append(line.strip().split('\t'))

#open CDS to pull file
CDS_to_pull = []
cat = set()

with open(os.path.join(directory,'CDS_to_pull.txt'),'r') as f:
	for line in f:
		CDS_to_pull.append(line.strip().split('\t'))
		if line.split('\t')[0] not in cat:
			cat.add(line.split('\t')[0])

with open(os.path.join(directory,'mappings_of_interest_divided_by_size.txt'),'w') as o:
	writer = csv.writer(o,delimiter='\t')
	for name in cat:
		for CDS in CDS_to_pull:
			if name == CDS[0]:
				for line in rm_table:
					if line[0] == CDS[1]:
						out_line = [name,line[0],line[1]]
						mapping_values = line[2:]
						for data in mapping_values:
							out_line.append(float(data)/float(line[1]))
						writer.writerow(out_line)
