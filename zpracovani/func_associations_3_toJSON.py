import json
import genes_col

#blattner2uniqueID
b2u = genes_col.blattner2uniqueID(genes_col.read_col_file('data/genes.col'))
#uniqueID2position
u2p = genes_col.uniqueID2position(genes_col.read_col_file('data/genes.col'))
a = genes_col.associations(b2u, u2p, genes_col.read_col_file('data/func_associations_3.col'))
for value in a.values():
	print json.dumps(value.toJSONobject())