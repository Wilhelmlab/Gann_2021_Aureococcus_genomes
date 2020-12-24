#reform tRNA-scan

#imports
import os 
import csv

#directory
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Final_assemblies/Genomes/CCMP1984'

#open out file and in file 
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	#open tRNA file
	with open(os.path.join(directory,'CCMP1984_tRNA'),'r') as f:
		
		count = 0
		for line in f:
			if line.startswith('CCMP'):
				count = count + 1
				data = line.strip().split('\t')
				out_line = [data[0],'tRNA-scan','tRNA']
				if int(data[2]) < int(data[3]):
					out_line.append(data[2])
					out_line.append(data[3])
					out_line.append('.')
					out_line.append('+')
					out_line.append('.')
					more_data = data[4] + ' (' + data[5] + ')'
					if len(data) == 10:
						more_data += ' pseudo'
					out_line.append(more_data)
				if int(data[2]) > int(data[3]):
					out_line.append(data[3])
					out_line.append(data[2])
					out_line.append('.')
					out_line.append('-')
					out_line.append('.')
					more_data = data[4] + ' (' + data[5] + ')'
					if len(data) == 10:
						more_data += ' pseudo'
					out_line.append(more_data)
				writer.writerow(out_line)

with open('CCMP1984_tRNA_for_gff.txt','w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')

quit()