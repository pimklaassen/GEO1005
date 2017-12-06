import urllib as url
from lxml import etree
import gzip, datetime, time, json

rotterdam = True

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


def record(mints):
	time_string = datetime.datetime.today().strftime('%d-%m')
	filename = time_string + ' recording {} minutes.txt'.format(str(mints))
	output = open(filename, 'w')

	start = datetime.datetime.now()
	end = start + datetime.timedelta(minutes=mints)

	while datetime.datetime.now() < end:
		open_bridges = get_bridge_info()

		if open_bridges:
			for open_bridge in open_bridges:
				json_string = json.dumps(open_bridge)
				print json_string
				output.write(json_string + '\n')
		else:
			print 'no open bridges in rotterdam'
		time.sleep(60)
	output.close()

record(60)
