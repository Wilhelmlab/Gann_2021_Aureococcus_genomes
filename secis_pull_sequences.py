#pull 10kb before the SECIS elements determined from online server 

#imports 
import os 
import csv 
from Bio.Seq import Seq

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Selenoproteins'

#get all files in the directory 
files = os.listdir(directory)

#strains 
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984']


#for each strain pull the secis element locations, and strand from fasta headers
#pull the sequences as well from the assembly file 

for strain in strains:
	#open SECIS file and make a data table 
	secis_table = []

	for file in files:
		if file.startswith(strain):
			if '_original_loose.fasta' in file:
				with open(os.path.join(directory,file),'r') as f:
					for line in f:
						if line.startswith('>'):
							secis_table.append(line.strip().split(' '))

	#pull all sequences from _assembly file 
	fasta_dict = dict()
	key = ""

	for file in files:
		if file.startswith(strain):
			if '_assembly.fasta' in file:
				with open(os.path.join(directory,file),'r') as f:
					for line in f:
						if line.startswith('>'):
							key = line.strip()
							fasta_dict[key] = ""
						else:
							fasta_dict[key] += line.strip()

	#for each line in secis table pull out genome chunk 
	out_dict = dict()
	dummy_dict = dict()
	for line in secis_table:
		chromosome = line[1].strip('chromosome:')
		strand = line[2].strip('strand:')
		start = int(line[3].strip('positions:').split('-')[0])
		end = int(line[3].strip('positions:').split('-')[1])

		name = '>' + chromosome + '_' + strand + '_' + str(start) + '_' + str(end)
		out_seq = ""

		#pull out the genome chunk 
		if strand == '+':
			for key in fasta_dict:
				if chromosome == key.strip('>'):
					check = start - 10000 
					if check < 0:
						out_seq = fasta_dict[key][:end]
					else:
						out_seq = fasta_dict[key][start-10000:end]
					out_dict[name] = out_seq
					dummy_dict[name] = out_seq
		if strand == '-':
			for key in fasta_dict:
				if chromosome == key.strip('>'):
					check = end + 10000
					if check > len(fasta_dict[key]):
						out_seq = fasta_dict[key][start:]
					else:
						out_seq = fasta_dict[key][start:end + 10000]
					seq = Seq(out_seq)
					rev_seq = seq.reverse_complement()
					dummy_dict[name] = out_seq
					out_dict[name] = rev_seq



	out_dummy = strain + '_dummy.fasta'
	out_real = strain + '_real.fasta'

	with open(os.path.join(directory,out_real),'w') as o:
		for x in out_dict:
			o.write(x)
			o.write('\n')
			o.write(str(out_dict[x]))
			o.write('\n')


	with open(os.path.join(directory,out_dummy),'w') as o:
		for x in dummy_dict:
			o.write(x)
			o.write('\n')
			o.write(str(dummy_dict[x]))
			o.write('\n')