server_address = '83.220.137.136'
server_port = 47910 # server of vesseltracker
buffer_size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "starting connection on {} port {}".format(server_address, server_port)
s.connect((server_address, server_port))

#receive the data from the server and serve it to a file with one line = one signal
vdata = open("vesseldata.txt", "w")
vdata.close()
a=0
b=1000
while a<b:
    data = s.recv(buffer_size)
    #print data
    dlen = len(data)
    dcnt = data.count("{")
    while dcnt>0: #while loop implemented in case of collated expressions (showing "{" after "}")
        position = data.find("}")
        if dcnt == 1:
            #vdata = open("vesseldata.txt", "a")
            #vdata.write(data)
            dict = json.loads(data)
            #print "1", dict
            #print data
            #print "time",dict["time_received"]
            #vdata.close()
            dcnt -=1
        else:
            #vdata = open("vesseldata.txt", "a")
            #vdata.write(data[0:position])
            cntchck = data.count("}")
            if dcnt == 2 and not dcnt == cntchck: #for the case of ais signal split over two json messages
                data2 = s.recv(buffer_size)
                data = data+data2
                dcnt = data.count("{")
                cntchck = data.count("}")
                dlen = len(data)
            #print "dnct", dcnt, data
            dict = json.loads(data[0:position+1])
            #print "2", dict
            #print data
            #print "time",dict["time_received"]
            #vdata.close()
            data = data[position+2:dlen]
            dlen = len(data)
            #print "out", data
            dcnt -=1
        if "msgid" in dict.keys():
            print dict["msgid"], dict
            """if dict["msgid"] == 1 or dict["msgid"] == 2 or dict["msgid"] == 3:
                print 1, dict
            if dict["msgid"] == 5:
                print 5, dict
            if dict["msgid"] == 24:
                print 24, dict
            if dict["msgid"] == 18 or dict["msgid"] == 19:
                print 18, dict"""
    a+=1


