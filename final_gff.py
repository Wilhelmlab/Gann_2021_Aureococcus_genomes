#finalize the .gff files 

#imports 
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Final_assemblies/Genomes/CCMP1984'


#open sorted gff
with open(os.path.join(directory,'temp.gff'),'w') as o:
	writer = csv.writer(o,delimiter='\t')
	with open(os.path.join(directory,'CCMP1984_sorted.gff'),'r') as f:
		for line in f:
			data = line.strip().split('\t')
			if len(data) == 9:
				new = data[:8]
				new.append(data[8].split(';')[0].strip('ID='))
				writer.writerow(new)
			if len(data) > 9:
				new = data[:8]
				new.append(data[10])
				writer.writerow(new)


with open(os.path.join(directory,'CCMP1984_final.gff'),'w') as o:
	with open(os.path.join(directory,'temp.gff'),'r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove(os.path.join(directory,'temp.gff'))