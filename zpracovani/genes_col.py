import csv
import json
import sys

# http://stackoverflow.com/questions/19151/build-a-basic-python-iterator
def comment_eater(f):
	for l in f:
		if l.startswith('#'):
			continue
		else:
			yield l
	raise StopIteration

def read_col_file(path):
	reader = csv.DictReader(comment_eater(file(path, 'rt')), dialect="excel-tab")
	return reader

def printout_genes_gff3(genescol_reader):
	print '##gff-version   3'
	for record in genescol_reader:
		start = record['START-BASE']
		end = record['END-BASE']
		direction = '+'
		#print >> sys.stderr, start, end
		try:
			if int(start) > int(end):
				z = end
				end = start
				start = z
				direction = '-'
		except ValueError:
			print >> sys.stderr,'invalid start or end values:', start, end
			continue
		name = record['BLATTNER-ID']
		if name == '':
			name = 'unnamed'
		print '%(seqid)s\t%(source)s\t%(type)s\t%(start)s\t%(end)s\t%(score)s\t%(strand)s\t%(phase)s\t%(attributes)s' % {
			'seqid'		:'NC_000913',
			'source'	:'EcoCyc',
			'type'		:'gene',
			'start'		:start,
			'end'		:end,
			'score'		:'.',
			'strand'	:direction,
			'phase'		:'.',
			'attributes':'ID=%(id)s;Name=%(name)s' % {'id': record['UNIQUE-ID'], 'name': name}
		}

if __name__ == '__main__':
	printout_genes_gff3(read_col_file('test/test_genes.col'))

def blattner2uniqueID(genescol_reader):
	b2u = {}
	for record in genescol_reader:
		b2u[record['BLATTNER-ID']] = record['UNIQUE-ID']
	return b2u

if __name__ == '__main__':
	print blattner2uniqueID(read_col_file('test/test_genes.col'))

def uniqueID2position(genescol_reader):
	u2p = {}
	for record in genescol_reader:
		start = record['START-BASE']
		end = record['END-BASE']
		try:
			if int(start) > int(end):
				z = end
				end = start
				start = z
		except ValueError:
			print >> sys.stderr,'invalid start or end values:', start, end
			continue
		u2p[record['UNIQUE-ID']] = (start, end)
	return u2p

if __name__ == '__main__':
	print uniqueID2position(read_col_file('test/test_genes.col'))

class Gene():
	def __init__(self, ID, start, end):
		self.ID = ID
		self.Start = start
		self.End = end
	def toJSONobject(self):
		return {'ID':self.ID, 'Start':self.Start, 'End':self.End}

class Regulation():
	"""
	self.ID = ""
	self.Regulates = []
	self.RegulatedBy = []
	"""
	def __init__(self, ID, regulates, regulatedby):
		self.ID = ID
		self.Regulates = regulates
		self.RegulatedBy = regulatedby
	def __str__(self):
		return str(self.Regulates) + ' ' + str(self.RegulatedBy)
	def toJSONobject(self):
		jid = self.ID
		jregulates = [x.toJSONobject() for x in self.Regulates]
		jregulatedby = [x.toJSONobject() for x in self.RegulatedBy]
		return {'ID': jid, 'Regulates': jregulates, 'RegulatedBy': jregulatedby}

def append_to_regs(regs, gene):
	if gene.ID not in regs:
		regs[gene.ID] = Regulation(gene.ID, [], [])

def associations(b2u, u2p, assoccol_reader):
	regs = {}
	for record in assoccol_reader:
		tfgene = None
		rgene = None
		try:
			tfgeneid = b2u[record['tfgene']]
			rgeneid = b2u[record['rgene']]
			tfgene = Gene(tfgeneid, u2p[tfgeneid][0], u2p[tfgeneid][1])
			rgene = Gene(rgeneid, u2p[rgeneid][0], u2p[rgeneid][1])
		except KeyError:
			print >> sys.stderr, 'Cannot lookup gene in regulation', record['tfgene'], '->', record['rgene']
			continue
		append_to_regs(regs, tfgene)
		append_to_regs(regs, rgene)
		regs[tfgene.ID].Regulates.append(rgene)
		regs[rgene.ID].RegulatedBy.append(tfgene)
	return regs

if __name__ == '__main__':
	print
	b2u = blattner2uniqueID(read_col_file('test/test_genes.col'))
	u2p = uniqueID2position(read_col_file('test/test_genes.col'))
	a = associations(b2u, u2p, read_col_file('test/func_associations_3_test.col'))
	for key,value in a.items():
		print key ,':', value
	print
	for key,value in a.items():
		print key ,':', json.dumps(value.toJSONobject())