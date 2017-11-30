import urllib as url
from lxml import etree
import gzip, datetime, time

# print datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')

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
		if check_location(check):
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

def run(mins):
	pass
	start = datetime.datetime.now()

	now_open = []
	locations = []
	locations_dict = []

	while start + datetime.timedelta(minutes=mins) > datetime.datetime.now():
		check_open = get_bridge_info()
		if check_open == None:
			time.sleep(60)
			continue
		for bridge in check_open:
			if not bridge['id'] in now_open:
				now_open.append(bridge['id'])
			else:
				now_open.remove(bridge['id'])

			if not bridge['id'] in locations:
				locations_dict.append({'id': bridge['id'],
								  	   'lat': bridge['latitude'],
								  	   'lon': bridge['longitude']})
				locations.append(bridge['id'])
		print 'now open:'
		for br in now_open:
			print br
		time.sleep(60)

run(10)