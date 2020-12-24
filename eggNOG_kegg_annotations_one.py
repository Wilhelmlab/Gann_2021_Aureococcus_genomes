#getting data from the KEGG json 
#file to understand the ko terms
#found within the output from 
#eggNOG 

#imports
import os
import csv
import json 

#SEP's json parser
class Node:
    #__slots__='_taxid','_parent','_children','_merged'

    def __init__(self,ident):
        dat = ident.split(' ')
        self.name = dat[0]
        self._metadata = ' '.join(dat[1:])
        self._parent = None
        self._children = []
        self._merged=False

    def get_metadata(self):
        return(self._metadata)

    def get_children(self):
        return(self._children)

    def add_child(self,child):
        self._children.append(child)
    
    def get_parent(self):
        return(self._parent)

    def set_parent(self,parent):
        self._parent = parent
    
    def __repr__(self):
        children=','.join([str(node.name) for node in self._children])
        if children:
            children = '('+children+')'
        else:
            children = 'None'
        if not self._parent:
            parent = 'None'
        else:
            parent = str(self._parent.name)
        out = ''.join(['Node(ID=',str(self.name),
                        ', Parent ID=',parent,
                        ', metadata= ',self._metadata,
                        ', Children= ',children,')'])
        return(out)

def _recursion(node,children,name_node):
    for el in children:
        cname = el['name']
        cnode = Node(cname) #make child node
        cnode.set_parent(node) #assign parent
        node.add_child(cnode) #add child to node
        name_node[cnode.name] = cnode #map key to node
        if 'children' in el:
            _recursion(cnode,el['children'],name_node)
    

def load_tree(json_obj):
        '''
        Loads the Tree of Life from the db
        '''
        name_node={}
        
        name = json_obj['name']
        node = Node(name)
        name_node[node.name] = node #map key to node

        if 'children' in json_obj:
            _recursion(node,json_obj['children'],name_node)


        return(name_node)

#directory 
directory = 'C:/Users/egann/Desktop/Aureococcus_strains/Comparing_Proteomes/Annotations/eggNOG'

#open the kegg json file and make into a Node
with open(os.path.join(directory,'ko00001.json'),'r') as f:
	kegg_data = json.load(f)

kegg_node = load_tree(kegg_data)

#get list of all KEGG ko's from all a text file 
kegg_names = []

with open(os.path.join(directory,'kegg_ko_out.txt'),'r') as f:
	for line in f:
		kegg_names.append(line.strip().split('\t')[0])

del kegg_names[0]

#get all parent data for each kegg term 
#using SEP json parser 
kegg_by_ko = []

for kegg_name in kegg_names:
	node = kegg_node[kegg_name]
	by_ko = [kegg_name,node._metadata]
	while node.get_parent():
		node = node.get_parent()
		by_ko.append(node._metadata)
	kegg_by_ko.append(by_ko)

#write to an outfile 
#with open('temp.txt','w') as o:
#	writer = csv.writer(o,delimiter='\t')
#	writer.writerows(kegg_by_ko)

#clean up
#with open(os.path.join(directory,'ko_data.txt'),'w') as o:
#	with open('temp.txt','r') as f:
#		for line in f:
#			if line != '\n':
#				o.write(line)

#os.remove('temp.txt')


#for each strain make a dictionary with each protein and the 
#ko terms from the eggNOG table 
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','XP_']



all_qualifiers = []
all_ko = []


for strain in strains:
	#make a smaller table of just those in eggNOG table which
	#are from that strain 
	strain_table = []

	with open(os.path.join(directory,'eggNOG_table.txt'),'r') as f:
		for line in f:
			if line.strip().split('\t')[0].startswith(strain):
				strain_table.append(line.strip().split('\t'))

	strain_kos = []

	for line in strain_table:
		if line[8] != '':
			ko_data = (line[8].strip().split(','))
			for data in ko_data:
				strain_kos.append(data.strip('ko:'))
	
	found_kos = []
	not_found_kos = []


	to_remove = ['K00870','K07088','K06955','K06060','K01541']

	keep = []
	for ko in strain_kos:
		if ko not in to_remove:
			keep.append(ko)

	strain_by_ko = []

	for kegg_name in keep:
		node = kegg_node[kegg_name]
		by_ko = [kegg_name,node._metadata]
		while node.get_parent():
			node = node.get_parent()
			by_ko.append(node._metadata)
		strain_by_ko.append(by_ko)

	redundancies_removed_ko_data = []
	seen = set()

	for line in strain_by_ko:
		if line[0] not in seen: 
			seen.add(line[0])
			redundancies_removed_ko_data.append(line)

	#use the keep ko names
	#and the redundancies removed ko data to 
	#get the number of each line[3]
	line_three_data_all = []

	for ko in keep:
		for line in redundancies_removed_ko_data:
			if ko == line[0]:
				line_three_data_all.append(line[3])
				all_qualifiers.append(line[3])
				all_ko.append(line[0])


	#make a set of all the line three data 
	#and count the number in the all data 
	#write to an outfile 

	line_three_no_redundancies = list(set(line_three_data_all))

	#out = strain + '_descriptions_of_kegg_overview.txt'
	#with open(os.path.join(directory,out),'w') as o:
	#	for data in line_three_no_redundancies:
	#		o.write(data)
	#		o.write('\t')
	#		o.write(str(line_three_data_all.count(data)))
	#		o.write('\n')



all_qualifiers_no_redundancies = list(set(all_qualifiers))

#out = 'all_descriptions_of_kegg_overview.txt'
#with open(os.path.join(directory,out),'w') as o:
#	for data in all_qualifiers_no_redundancies:
#		o.write(data)
#		o.write('\t')
#		o.write(str(all_qualifiers.count(data)))
#		o.write('\n')


#get qualifiers for all ko terms
kegg_by_ko_all = []

for kegg_name in all_ko:
	node = kegg_node[kegg_name]
	by_ko = [kegg_name,node._metadata]
	while node.get_parent():
		node = node.get_parent()
		by_ko.append(node._metadata)
	kegg_by_ko_all.append(by_ko)


#open the files for pan and core genomes 
core_genome = set()
pan_genome = set()
pan_4_genome = set()
pan_3_genome = set()
pan_2_genome = set()
pan_1_genome = set()

with open(os.path.join(directory,'core_KEGG.txt'),'r') as f:
	for line in f:
		core_genome.add(line.strip())

with open(os.path.join(directory,'pan_KEGG.txt'),'r') as f:
	for line in f:
		pan_genome.add(line.strip())

with open(os.path.join(directory,'pan_4.txt'),'r') as f:
	for line in f:
		pan_4_genome.add(line.strip())

with open(os.path.join(directory,'pan_3.txt'),'r') as f:
	for line in f:
		pan_3_genome.add(line.strip())

with open(os.path.join(directory,'pan_2.txt'),'r') as f:
	for line in f:
		pan_2_genome.add(line.strip())

with open(os.path.join(directory,'pan_1.txt'),'r') as f:
	for line in f:
		pan_1_genome.add(line.strip())


#separate all data
pan_data = []
pan_data_three = []
core_data = []
core_data_three = []
pan_4_data = []
pan_4_data_three = []
pan_3_data = []
pan_3_data_three = []
pan_2_data = []
pan_2_data_three = []
pan_1_data = []
pan_1_data_three = []

for line in kegg_by_ko_all:
	if line[0] in core_genome:
		core_data.append(line)
		core_data_three.append(line[3])
	if line[0] in pan_genome:
		pan_data.append(line)
		pan_data_three.append(line[3])
	if line[0] in pan_4_genome:
		pan_4_data.append(line)
		pan_4_data_three.append(line[3])
	if line[0] in pan_3_genome:
		pan_3_data.append(line)
		pan_3_data_three.append(line[3])
	if line[0] in pan_2_genome:
		pan_2_data.append(line)
		pan_2_data_three.append(line[3])
	if line[0] in pan_1_genome:
		pan_1_data.append(line)
		pan_1_data_three.append(line[3])


pan_4_qualifiers_no_redundancies = list(set(pan_4_data_three))

out = 'pan_4_descriptions_of_kegg_overview.txt'
with open(os.path.join(directory,out),'w') as o:
	for data in pan_4_qualifiers_no_redundancies:
		o.write(data)
		o.write('\t')
		o.write(str(pan_4_data_three.count(data)))
		o.write('\n')

pan_3_qualifiers_no_redundancies = list(set(pan_3_data_three))

out = 'pan_3_descriptions_of_kegg_overview.txt'
with open(os.path.join(directory,out),'w') as o:
	for data in pan_3_qualifiers_no_redundancies:
		o.write(data)
		o.write('\t')
		o.write(str(pan_3_data_three.count(data)))
		o.write('\n')

pan_2_qualifiers_no_redundancies = list(set(pan_2_data_three))

out = 'pan_2_descriptions_of_kegg_overview.txt'
with open(os.path.join(directory,out),'w') as o:
	for data in pan_2_qualifiers_no_redundancies:
		o.write(data)
		o.write('\t')
		o.write(str(pan_2_data_three.count(data)))
		o.write('\n')

pan_1_qualifiers_no_redundancies = list(set(pan_1_data_three))

out = 'pan_1_descriptions_of_kegg_overview.txt'
with open(os.path.join(directory,out),'w') as o:
	for data in pan_1_qualifiers_no_redundancies:
		o.write(data)
		o.write('\t')
		o.write(str(pan_1_data_three.count(data)))
		o.write('\n')



#core_qualifiers_no_redundancies = list(set(core_data_three))

#out = 'core_descriptions_of_kegg_overview.txt'
#with open(os.path.join(directory,out),'w') as o:
#	for data in core_qualifiers_no_redundancies:
#		o.write(data)
#		o.write('\t')
#		o.write(str(core_data_three.count(data)))
#		o.write('\n')

#pan_qualifiers_no_redundancies = list(set(pan_data_three))

#out = 'pan_descriptions_of_kegg_overview.txt'
#with open(os.path.join(directory,out),'w') as o:
#	for data in pan_qualifiers_no_redundancies:
#		o.write(data)
#		o.write('\t')
#		o.write(str(pan_data_three.count(data)))
#		o.write('\n')

#core_seen = set()

#out = 'core_kegg_data.txt'
#with open('temp.txt','w') as o:
#	writer = csv.writer(o,delimiter='\t')
#	for data in core_data:
#		if data[0] not in core_seen:
#			writer.writerow(data)
#			core_seen.add(data[0])

#with open(os.path.join(directory,out),'w') as o:
#	with open('temp.txt','r') as f:
#		for line in f:
#			if line != '\n':
#				o.write(line)

#os.remove('temp.txt')

#pan_seen = set()

#out = 'pan_kegg_data.txt'
#with open('temp.txt','w') as o:
#	writer = csv.writer(o,delimiter='\t')
#	for data in pan_data:
#		if data[0] not in pan_seen:
#			writer.writerow(data)
#			pan_seen.add(data[0])

#with open(os.path.join(directory,out),'w') as o:
#	with open('temp.txt','r') as f:
#		for line in f:
#			if line != '\n':
#				o.write(line)

#os.remove('temp.txt')