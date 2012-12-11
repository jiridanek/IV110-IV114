import func_associations_3_toJSON
a = func_associations_3_toJSON.a
u2p = func_associations_3_toJSON.u2p

regulators = []
regulees = []

for id, reg in a.iteritems():
	start = u2p[reg.ID][0]
	end = u2p[reg.ID][1]
	for _ in reg.RegulatedBy:
		regulees.append(start)
		regulees.append(end)
	for g in reg.Regulates:
		regulators.append(start)
		regulators.append(end)

with open("regulators.txt", 'wt') as f:
	for r in regulators:
		print >> f, r
		
with open("regulees.txt", 'wt') as f:
	for r in regulees:
		print >> f, r