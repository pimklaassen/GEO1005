import json

class vesselParser():

	def __init__(self, openFileObject):
		self.lines = openFileObject.readlines()
		self.time_slot = []
		self.dict_list = []
		self.init_time = 832332

	def parse(self):
		for line in self.lines:
			d = eval(line)
			t = (int(str(d['time'])[4:-3]) - self.init_time) / 10.0
			d['time'] = t
			self.time_slot.append(t)
			self.dict_list.append(d)

	def generator(self):
		for t in self.time_slot:
			for d in self.dict_list:
				if d['time'] == t:
					yield d


lst = []
def fix(f):
	f = open(f, 'r')
	l = f.readlines()
	for line in l:
		line = line.replace(' ', '')
		line = line.replace('@', '')
		line = line.replace('koninginne', '"koninginne"')
		line = line.replace('erasmus', '"erasmus"')
		parts = line.split(':')
		replacement_parts = parts[3].split(',')
		replacement = '"' + replacement_parts[0] + '",' + replacement_parts[1]
		parts[3] = replacement
		line = ':'.join(parts)
		lst.append(line)