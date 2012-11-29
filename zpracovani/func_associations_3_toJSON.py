import genes_col

b2u = genes_col.blattner2uniqueID(genes_col.read_col_file('data/genes.col'))
a = genes_col.associations(b2u, genes_col.read_col_file('data/func_associations_3.col'))
for value in a.values():
	print value.toJSONobject()