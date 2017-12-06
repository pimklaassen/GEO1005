import urllib as url
from lxml import etree
import gzip, datetime, time, pprint, progressbar

rotterdam = False

def check_location(string):
	if string[6:11] == 'NLRTM':
		return True
	elif string[0:3] == 'GRT':
		return True
	return False

def get_bridge_info():
	open_bridges = []
	root = None
	nodes = None

	try:
		response = url.urlretrieve('http://opendata.ndw.nu/brugopeningen.xml.gz', 'feed.xml.gz')
		xml = None
		with gzip.open('feed.xml.gz', 'rb') as feed:
			xml = feed.read()
		root = etree.fromstring(xml)
	except:
		return

	try:
		nodes = root.iter('{http://datex2.eu/schema/2/2_0}situation')
	except:
		return

	for node in nodes:
		check = None
		bridge_id = None
		timestamp = None
		bridge_la = None
		bridge_lo = None

		try:
			check = node.attrib['id']
		except:
			continue
		if not check_location(check) == rotterdam:
			continue
		bridge_id = check

		timestamp = datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')

		try:
			for el in node.iter('{http://datex2.eu/schema/2/2_0}latitude'):
				bridge_la = float(el.text)
				break
		except:
			bridge_la = -9999

		try:
			for el in node.iter('{http://datex2.eu/schema/2/2_0}longitude'):
				bridge_lo = float(el.text)
				break
		except:
			bridge_lo = -9999

		open_bridges.append({'id': bridge_id, 
							 'open': str(timestamp),
							 'latitude': bridge_la,
							 'longitude': bridge_lo})

	return open_bridges

for i in xrange(1):
	now = get_bridge_info()
	if not now:
		print 'no bridges open'
	else:
		output = open('output_qgis.csv', 'r')
		content = output.readlines()
		output.close()

		new_content = []
		print content
		if content:
			id_names = [l.split(';')[0] for l in content]
			for bridge in now:
				if bridge['id'] not in id_names:
					new_content.append('{};{};{};{}\n'.format(bridge['id'],
														      'True',
														      bridge['latitude'],
														      bridge['longitude']))
				else:
					
		else:
			new_content.append('NULL;NULL;NULL;NULL')

		output = open('output_qgis.csv', 'w')
		for line in new_content:
			output.write('{}'.format(line))
		output.close()

	# time.sleep(1)
