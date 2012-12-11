import json
import genes_col

#blattner2uniqueID
b2u = genes_col.blattner2uniqueID(genes_col.read_col_file('data/genes.col'))
#uniqueID2position, ""exported""
u2p = genes_col.uniqueID2position(genes_col.read_col_file('data/genes.col'))
# a is ""exported""
a = genes_col.associations(b2u, u2p, genes_col.read_col_file('data/func_associations_3.col'))

if __name__ == '__main__':
	for value in a.values():
		print json.dumps(value.toJSONobject())