#counts the number of each COG one letter descripter in each stain 

#imports
import os 
import csv 

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/COG_counts'

#open eggNOG table 
eggNOG_table = []

with open(os.path.join(directory,'eggNOG_table.txt'),'r') as f: 
	for line in f: 
		eggNOG_table.append(line.split('\t'))

#strains
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','XP_']

#get all the one letter codes
seen_one_letter = set()

for line in eggNOG_table:
	if line[20] not in seen_one_letter:
		if len(line[20]) != 1:
			if line[20] != 'COG cat':
				new  = list(line[20])
				for data in new:
					if data not in seen_one_letter:
						seen_one_letter.add(data)
		else:
			seen_one_letter.add(line[20])

seen_one_letter = list(seen_one_letter)

#split the table by strain, and count the number of 
#each COG one letter 
out = []

for strain in strains: 
	#out 
	out_strain = [strain]
	#strain table 
	strain_table = []

	for line in eggNOG_table:
		if line[0].startswith(strain):
			strain_table.append(line)
	
	#for each one letter cog, count in strain table
	for one_letter in seen_one_letter:
		count = 0
		for line in strain_table:
			data = list(line[20])
			if one_letter in data:
				count = count + 1
		out_strain.append(str(count))

	out.append(out_strain)

seen_one_letter.insert(0,'COG code')
out.insert(0,seen_one_letter)

#write to an out file
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(zip(*out))

with open(os.path.join(directory,'COG_counts_by_strain.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')