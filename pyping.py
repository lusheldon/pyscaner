#!/usr/bin/python
#--*-- coding: utf-8 --*--
import os, sys, socket, struct, select, time

def pyping():
	count=0		#default value
	timeout=4
	if len(sys.argv)==1:
		usage()
	dest = sys.argv[1]
	try:
		for i in range(len(sys.argv)):
			if sys.argv[i] == "-c":
				count = int(sys.argv[i+1])
			elif sys.argv[i] == "-t":
				timeout = float(sys.argv[i+1])
			elif sys.argv[i] == "-i":
				interval = float(sys.argv[i+1])
			else:
				pass
	except:
		usage()
	"""need more option"""
	
	doping(dest, count, timeout, interval)


def probe(ip):
    PID = os.getpid()
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1) # get the socket, 1 is the protocol number
    for i in range(4):
        time.sleep(0.02)
        packet = packIcmp(ip, PID)   # pack the pakcet
        sock.sendto(packet, (ip,1))          #send the packet
        result = recvicmp(sock, PID, 0.1)    #receive the ICMP reply 
        if result == 0:
            return False
        else:
            return True
	
def usage():
	print "Usage:"
	print "\t./pyping destination [-c count] [-t second]"
	print "\tExample: pyping 192.168.0.1 -c 4 -t 0.5"
	print "\tExample: pyping www.google.com -t 2"
	exit()

def doping(dest, count, timeout, interval):

	host = resolve_host(dest)  # get the IP

	PID = os.getpid()
	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1) # get the socket, 1 is the protocol number
	if count == 0:
		count = 65535 
	print "Pinging start!"
	for i in xrange(count):
		time.sleep(interval)
		packet = packIcmp(host, PID)   # pack the pakcet
		print "Pinging",dest,"attempts",i+1,
		sock.sendto(packet, (host,1))          #send the packet
		result = recvicmp(sock, PID, timeout)    #receive the ICMP reply 
		if result == 0:
			print "get reply timeout!"
		else:
			print "get reply in ",result, "ms"
def recvicmp(sock, PID, timeout):
	while True:
		clockStart = time.time()
		s = select.select([sock], [], [], timeout)
		if s[0]==[]:
			return 0
		clockStop = time.time()
		received, addr = sock.recvfrom(1024)
		timeSent = unpackIcmp(received, PID)
		if timeSent != 0:
			return clockStop-timeSent
		if clockStop-clockStart>timeout:
			return 0
			
def unpackIcmp(obj, PID):
	icmpHeader = obj[20:28]
	type, code, checksum, packetID, sequence = struct.unpack(
		"bbHHh", icmpHeader
	)
	if type != 8 and packetID == PID:
		bytesInDouble = struct.calcsize("d")
		return struct.unpack("d", obj[28:28 + bytesInDouble])[0]
	else:
		return 0
			
def packIcmp(host, PID):
	"""not much understand these code"""
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	my_checksum = 0
	#request type: 8
	header = struct.pack("bbHHh", 8, 0, my_checksum, PID, 1)
	bytesInDouble = struct.calcsize("d")
	data = (192 - bytesInDouble) * "Q"
	data = struct.pack("d", time.time()) + data
	
	#get the new checksum
	my_checksum = checksum(header + data)
	header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), PID, 1)
	return header + data

def checksum(source_string):
	"""
	These codes are copied from samuel/python-ping
	"""
	sum = 0
	countTo = (len(source_string)/2)*2
	count = 0
	while count<countTo:
		thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
		sum = sum + thisVal
		sum = sum & 0xffffffff # Necessary?
		count = count + 2
	
	if countTo<len(source_string):
		sum = sum + ord(source_string[len(source_string) - 1])
		sum = sum & 0xffffffff # Necessary?
	
	sum = (sum >> 16)  +  (sum & 0xffff)
	sum = sum + (sum >> 16)
	answer = ~sum
	answer = answer & 0xffff
	
	# Swap bytes. Bugger me if I know why.
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

def resolve_host(dest):
	try:
		if socket.inet_aton(dest):
			return dest
	except:
		try:
			return socket.gethostbyname(dest)
		except:
			print "Host ip resolve failed, pyping exited!"
			exit()
if __name__=="__main__":
	pyping()