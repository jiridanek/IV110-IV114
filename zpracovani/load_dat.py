#usr/bin/python

def is_list(list):
	return hasattr(list, "append")

def load_BioCyc_attribute_value(path):
	data = []
	with open(path) as f:
		line = f.readline()
		d = {}
		previous_key = None
		while line != '':
			line = line.strip()
			if line.startswith('#'):
				pass
			elif line.startswith('//'):
				data.append(d)
				d = {}
			elif line.startswith('/'):
				d[previous_key].append(line[1:])
			else:
				transformed_line = line.split(' - ')
				key = transformed_line[0]
				value = ' - '.join(transformed_line[1:])
				if key in d:
					d[key].append(value)
				else:
					d[key] = [value]
				previous_key = key
			line = f.readline()
		if len(d) != 0:
			data.append(d)
	return data

a = load_BioCyc_attribute_value("test/test.dat")
print a	