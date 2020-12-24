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
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(kegg_by_ko)

#clean up
with open(os.path.join(directory,'ko_data.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')


#get the name of all proteins for all strains
protein_names = []

with open(os.path.join(directory,'all_plus_ref.fasta'),'r') as f: 
	for line in f:
		if line.startswith('>'):
			protein_names.append(line.strip().split(' ')[0].strip('>'))

#make a data table of the eggNOG output file 
eggNOG_table = []

with open(os.path.join(directory,'eggNOG_table.txt'),'r') as f:
	for line in f:
		eggNOG_table.append(line.split('\t'))


#make tiers for an out file to write 
#split kegg by ko data 
tier_one_classification = []
tier_two_classification = []


for data in kegg_by_ko:
	if data[4] not in tier_one_classification:
		tier_one_classification.append(data[4])
	if data[3] not in tier_two_classification:
		tier_two_classification.append(data[3])

for data in tier_one_classification:
	print(data)

#for each strain make a dictionary with each protein and the 
#ko terms from the eggNOG table 
strains = ['CCMP1707','CCMP1794','CCMP1850','CCMP1984','XP_']

t1_out = []
t2_out = []


for strain in strains:
	#make a smaller table of just those in eggNOG table which
	#are from that strain 
	strain_table = []

	for line in eggNOG_table:
		if line[0].startswith(strain):
			strain_table.append(line)

	#get the names of the proteins for that strain

	strain_proteins = []

	for protein in protein_names:
		if protein.startswith(strain):
			strain_proteins.append(protein)

	#for each protein from the strain 
	#determine how many have a ko number assigned 
	#to them 
	kegg_ko = []

	none_count = 0
	some_count = 0
	for protein in strain_proteins:
		in_eggNOG = 0
		in_eggNOG_with_kegg = 0
		for line in strain_table:
			if protein == line[0]:
				in_eggNOG = in_eggNOG + 1
				if line[8] != '':
					in_eggNOG_with_kegg = in_eggNOG_with_kegg + 1
					kegg_ko_data = line[8].split(',')
					for data in kegg_ko_data:
						kegg_ko.append(data.strip('ko:'))
					some_count = some_count + 1
		if in_eggNOG == 0 or in_eggNOG_with_kegg == 0:
			none_count = none_count	+ 1
	
	#print general stats about kegg things
	print(strain)
	print('number of proteins')
	print(len(strain_proteins))
	print('proteins with ko')
	print(some_count)
	print('proteins without ko')
	print(none_count)
	print('\n')

	#for each tier count the number
	#of ko terms from the strain 
	#are in that classification 

	t1_strain = [strain]
	t2_strain = [strain]


	for term in tier_one_classification:
		t1_count = 0
		for data in kegg_by_ko:
			if data[4] == term:
				print(term)
				print('ok')
				t1_count = t1_count + 1
		t1_strain.append(t1_count)

	print('t1 done')
	#add to out files
	t1_out.append(t1_strain)


#write tiers to out file 
with open('temp.txt','w') as o:
	writer = csv.writer(o,delimiter='\t')
	writer.writerows(zip(*t1_out))

with open(os.path.join(directory,'tier_one_KEGG_out.txt'),'w') as o:
	with open('temp.txt','r') as f:
		for line in f:
			if line != '\n':
				o.write(line)

os.remove('temp.txt')
