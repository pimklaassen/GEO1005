import socket, time, json

ip = '83.220.137.136'
port = 47910
record_time = 60 * 60

s = socket.socket()
s.connect((ip, port))
buff = 4096

test_f = open('vessel_datastream_1900.txt', 'w')

delta = time.time() + record_time
while time.time() < delta:
	msg = s.recv(buff)
	if msg:
		test_f.write(msg.strip())

s.close()
test_f.close()

