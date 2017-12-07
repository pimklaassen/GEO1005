import json

def json2csv(filename_in, filename_out):
	raw_json = open(filename_in, 'r')
	json_lines = raw_json.readlines()
	raw_json.close()

	out_file = open(filename_out, 'w')
	out_file.write('lat,lon,id,time\n')

	for line in json_lines:
		d = json.loads(line)
		out_file.write('{},{},{},{}\n'.format(d['latitude'],
											  d['longitude'],
											  d['id'],
											  d['open']))

	out_file.close()
