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
	def toJSONarray(self):
		return json.dumps([self.ID, self.Regulates, self.RegulatedBy])
	def toJSONobject(self):
		return json.dumps({'ID':self.ID, 'Regulates':self.Regulates, 'RegulatedBy':self.RegulatedBy})

def associations(b2u, assoccol_reader):
	regs = {}
	for record in assoccol_reader:
		tfgene = None
		rgene = None
		try:
			tfgene = b2u[record['tfgene']]
			rgene = b2u[record['rgene']]
		except KeyError:
			print >> sys.stderr, 'Cannot lookup gene in regulation', record['tfgene'], '->', record['rgene']
			continue
		if tfgene in regs:
			regs[tfgene].Regulates.append(rgene)
		else:
			regs[tfgene] = Regulation(tfgene, [rgene], [])
		if rgene in regs:
			regs[rgene].RegulatedBy.append(tfgene)
		else:
			regs[rgene] = Regulation(rgene, [], [rgene])
	return regs

if __name__ == '__main__':
	print
	b2u = blattner2uniqueID(read_col_file('test/test_genes.col'))
	a = associations(b2u, read_col_file('test/func_associations_3_test.col'))
	for key,value in a.items():
		print key ,':', value
	print
	for key,value in a.items():
		print key ,':', value.toJSONobject()