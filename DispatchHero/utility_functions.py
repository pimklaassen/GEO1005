#----------------------------------------------------#
#      Class for parsing the bridges is timeSlots    #
#----------------------------------------------------#

class BridgeParser():

	def __init__(self, openFileObject):
		self.file = openFileObject
		self.timeSlots = []
		self.timeDict = {}

	def parse(self):
		self.fh = self.file.readlines()
		self.file.close()

		for line in self.fh:
			dictObject = eval(line.strip())
			openingTime = dictObject['open']
			if not openingTime in self.timeSlots:
				self.timeSlots.append(openingTime)
				self.timeDict[openingTime] = []

		for openingTime in self.timeSlots:
			for line in self.fh:
				dictObject = eval(line.strip())
				if dictObject['open'] == openingTime:
					self.timeDict[openingTime].append(dictObject['id'])

	def generator(self):
		for time in self.timeSlots:
			yield self.timeDict[time]