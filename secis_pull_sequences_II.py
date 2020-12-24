#Pull out the selenoproteins top hits from

#imports 
import os
import csv

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Selenoproteins'

#get all subjects from db fasta file 
fasta_dict = dict()
key = ""

with open(os.path.join(directory, 'Aureococcus_selenoproteins.fasta'),'r') as f: 
	for line in f: 
		if line.startswith('>'):
			key = line.strip().split(' ')[0].strip('>')
			fasta_dict[key] = ""
		else:
			fasta_dict[key] += line.strip()

#smaller blast table 
top_hit = []
seen = []

with open(os.path.join(directory, 'secis_blastx_table_chunks_forward.txt'),'r') as f: 
	for line in f: 
		if line.strip().split('\t')[0] not in seen:
			if int(line.strip().split('\t')[12]) > 0:
				seen.append(line.strip().split('\t')[0])
				top_hit.append(line.strip().split('\t'))

full_hits_all_subjects = []

for line in top_hit:
	sub = line[1]
	query = line[0]
	with open(os.path.join(directory, 'secis_blastx_table_chunks_forward.txt'),'r') as f: 
		for line in f: 
			if line.strip().split('\t')[0] == query:
				if line.strip().split('\t')[1] == sub:
					full_hits_all_subjects.append(line.strip().split('\t'))

with open(os.path.join(directory, 'temp.txt'),'w') as o:
	writer = csv.writer(o,delimiter='\t') 
	writer.writerows(full_hits_all_subjects)

with open(os.path.join(directory, 'top_hits_all_sub.txt'),'w') as o:
	with open(os.path.join(directory, 'temp.txt'),'r') as f:
		for line in f: 
			if line != '\n':
				o.write(line)

os.remove(os.path.join(directory, 'temp.txt'))


final_out_table_data = []

for query in seen: 
	out_table_data = [query]
	#pull out only lines from query table 
	query_table = []


	for line in full_hits_all_subjects:
		if line[0] == query:
			query_table.append(line)

	#get subject length 
	subject = query_table[0][1]
	out_table_data.append(subject)

	sub_length = ""

	for sub in fasta_dict:
		if sub == subject:
			sub_length = len(fasta_dict[sub])

	#sum the read frame, if < 0 pull out largeest
	#from line[6] and the smallest from line[7]
	#if >0 do the opposite
	line_six_data = []
	line_seven_data = []
	qf_count = 0
	for data in query_table:
		line_six_data.append(int(data[6]))
		line_seven_data.append(int(data[7]))
		qf_count = qf_count	+ int(data[12])

	if qf_count > 0:
			out_table_data.append('+')
			#sort line[6] data by smallest
			sorted_six = sorted(line_six_data)
			#and line[7] data by largest
			sorted_seven = sorted(line_seven_data, reverse=True)
			size = sorted_seven[0] - sorted_six[0]

			out_table_data.append(sorted_six[0])
			out_table_data.append(sorted_seven[0])
			out_table_data.append(size)
			out_table_data.append(float(size/3))
			out_table_data.append(float(size/3/sub_length))


	if qf_count	< 0:
			out_table_data.append('-')
			#sort line[6] data by largest
			sorted_seven = sorted(line_seven_data)
			#and line[7] data by smallest
			sorted_six = sorted(line_six_data, reverse=True)
			size = sorted_six[0] - sorted_seven[0]
			out_table_data.append(sorted_six[0])
			out_table_data.append(sorted_seven[0])
			out_table_data.append(size)
			out_table_data.append(float(size/3))
			out_table_data.append(float(size/3/sub_length))

	if out_table_data[7] >= 0.4:
			final_out_table_data.append(out_table_data)


with open(os.path.join(directory, 'temp.txt'),'w') as o:
	writer = csv.writer(o,delimiter='\t') 
	writer.writerows(final_out_table_data)

with open(os.path.join(directory, 'top_hits_combined_data.txt'),'w') as o:
	with open(os.path.join(directory, 'temp.txt'),'r') as f:
		for line in f: 
			if line != '\n':
				o.write(line)

os.remove(os.path.join(directory, 'temp.txt'))


#get all secis_chunks_sequences 
secis_chunk_dict = dict()
key = ""

with open(os.path.join(directory,'all_secis_genome_chunks_forward.fasta'),'r') as f: 
	for line in f:
		if line.startswith('>'):
			key = line.strip().strip('>')
			secis_chunk_dict[key] = ""
		else:
			secis_chunk_dict[key] += line.strip()

#pull out the chunks of the chunk sequence for the protein 
with open(os.path.join(directory,'Selenoprotein_hit_chunk.fasta'),'w') as o:
	for line in final_out_table_data:
		#write out name
		for key in secis_chunk_dict:
			if line[0] == key:
				if line[2] == '+':
					out_name = '>' + line[0] + '_' + line[2] + '_' + str(line[3]) + '_' + str(line[4])
					sequence = secis_chunk_dict[key][int(line[3])-1:int(line[4])]
					o.write(out_name)
					o.write('\n')
					o.write(sequence) 
					o.write('\n')
				if line[2] == '-':
					out_name = '>' + line[0] + '_' + line[2] + '_' + str(line[4]) + '_' + str(line[3])
					secis_chunk_dict[key][int(line[4])+1:int(line[3])]
					o.write(out_name)
					o.write('\n')
					o.write(sequence) 
					o.write('\n')