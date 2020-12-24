#Edit .gff table and renumber coding sequences and add in the protein data 
#...stepwise probably

#imports 
import os 
import csv 

#files directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Final_assemblies/Genomes/CCMP1984'


#first open the .gff file and get all contigs
#get the number the contig is (it is based on size)
#and renumber a list of list by that number 
contigs = []
seen = set()

with open(os.path.join(directory,'CCMP1984_gff_proteins.gff'),'r') as f:
	for line in f:
		if line.strip().split('\t')[0] not in seen:
			seen.add(line.strip().split('\t')[0])
			contigs.append([line.strip().split('\t')[0],int(line.strip().split('\t')[0].split('_')[1])])

#sort list of list by second term
#which is the contig number 
contigs.sort(key=lambda x:x[1])


	#for each contig open the file and pull out only those lines that start with the contig
	#then rename the last column, and reorder based on the start sequence

gene_table_to_add_to = []

with open('temp.gff','w') as o:
	writer = csv.writer(o,delimiter='\t')
	for contig in contigs:
		#make smaller table 
		smaller_table = []
		with open(os.path.join(directory,'CCMP1984_gff_proteins.gff'),'r') as f:
				for line in f:
					if line.strip().split('\t')[0] == contig[0]:
						smaller_table.append(line.strip().split('\t'))

		header = smaller_table[0]

		del smaller_table[0]

		#pull out all gene rows 
		gene_table = []

		for line in smaller_table:
			if line[2] == 'gene':
				gene_table.append(line)

		#sort gene table based on start of sequence
		gene_table.sort(key=lambda x:int(x[3]))

		
		#make a new out_table with the now correct order
		out_table = [header]

		count = 1
		for line in gene_table:
	
			for data in smaller_table:
				if data[8].split(';')[0].split(':')[0].replace('-mRNA-1','').replace('ID=','') == line[8].split(';')[0].split(':')[0].replace('-mRNA-1','').replace('ID=',''):
					out_data = data
					new_ID = contig[0] + '_' + str(count)
					out_data.append(data[8].split(';')[0].split(':')[0].replace('-mRNA-1','').replace('ID=',''))
					out_data.append(new_ID)
					out_table.append(out_data)
			

			new_line = line
			new_line.append(line[8].split(';')[0].split(':')[0].replace('-mRNA-1','').replace('ID=',''))
			new_line.append(new_ID)
			gene_table_to_add_to.append(new_line)
			count = count + 1

		writer.writerows(out_table)

#remove excess lines in the file 
with open('CCMP1984_sorted.gff','w') as o:
	with open('temp.gff','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.gff')


#use the gene_table_to_add_to to pull CDS and protein data from their respective files
#open files and make dictionaries for both 
protein_dict = dict()
key = ""

with open(os.path.join(directory,'CCMP1984_proteins.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			key = line.strip().split(' ')[0]
			protein_dict[key] = ""
		else:
			protein_dict[key] += line.strip()

transcript_dict = dict()
key = ""

with open(os.path.join(directory,'CCMP1984_transcripts.fasta'),'r') as f:
	for line in f:
		if line.startswith('>'):
			key = line.strip().split(' ')[0]
			transcript_dict[key] = ""
		else:
			transcript_dict[key] += line.strip()


#open new temp out file 
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	for line in gene_table_to_add_to:
		to_check = line[9] + '-mRNA-1'
		out_line = line
		for key in protein_dict:
			if key.strip('>') == to_check:
				out_line.append(protein_dict[key])
		for key in transcript_dict:
			if key.strip('>') == to_check:
				out_line.append(transcript_dict[key])
		if len(out_line) != 1:
			writer.writerow(out_line)


#remove not needed lines
with open('CCMP1984_genes_with_seq.txt','w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')