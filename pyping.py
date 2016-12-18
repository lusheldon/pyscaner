#!/usr/bin/python
#--*-- coding: utf-8 --*--
import os, sys, socket, struct, select, time, array
class Ping():

	
	def __init__(self, dest, count = 4, interval = 0.01, timeout = 0.1):
		self.PID = os.getpid()
		self.count = count
		self.dest = dest
		self.interval = interval
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1) # get the socket, 1 is the protocol number
	
	
	def probe(self):
		for i in range(self.count):
			time.sleep(self.interval)
			packet = self.packIcmp()   # pack the pakcet
			self.sock.sendto(packet, (self.dest,1))          #send the packet
			result = self.recvicmp()    #receive the ICMP reply 
			if result == 0:
				return False
			else:
				return True
		
		
	def doping(self):
		host = self.resolve_host()  # get the IP
		if self.count < 1:
			self.count = 65535 
		print "Pinging start!"
		for i in xrange(self.count):
			time.sleep(self.interval)
			packet = self.packIcmp()   # pack the pakcet
			print "Pinging",self.dest,"attempts",i+1,
			self.sock.sendto(packet, (host,1))          #send the packet
			result = self.recvicmp()    #receive the ICMP reply 
			if result == 0:
				print "get reply timeout!"
			else:
				print "get reply in %.2f ms" %(result*1000)
				
				
	def recvicmp(self):
		while True:
			clockStart = time.time()
			s = select.select([self.sock], [], [], self.timeout)
			if s[0]==[]:
				return 0
			clockStop = time.time()
			received, addr = self.sock.recvfrom(1024)
			timeSent = self.unpackIcmp(received)
			if timeSent != 0:
				return clockStop - timeSent
			if clockStop-clockStart>self.timeout:
				return 0
		
		
	def unpackIcmp(self, recv):
		icmpHeader = recv[20:28]
		type, code, checksum, packetID, sequence = struct.unpack(
			"bbHHh", icmpHeader
		)

		if type == 0 and packetID == self.PID:
			return struct.unpack("d", recv[28:36])[0]
		else:
			return 0
	
	
	def packIcmp(self):
		# Header is type (8), code (8), checksum (16), id (16), sequence (16)
		cksum = 0
		#request type: 8
		header = struct.pack("bbHHh", 8, 0, cksum, self.PID, 1)
		data = struct.pack("d", time.time())
		#get the new checksum
		cksum = checksum(header + data)
		header = struct.pack("bbHHh", 8, 0, socket.htons(cksum), self.PID, 1)
		return header + data
		
	def resolve_host(self):
		try:
			if socket.inet_aton(self.dest):
				return self.dest
		except:
			try:
				return socket.gethostbyname(dest)
			except:
				print "Host ip resolve failed, pyping exited!"
				exit()

				
			
def checksum(packet):
	'''caculate the checksum'''
	if len(packet) & 1:
		packet = packet + '\0'
	words = array.array('h', packet)
	sum = 0
	for word in words:
		sum += (word & 0xffff)
	sum = (sum >> 16) + (sum & 0xffff)
	sum = sum + (sum >> 16)
	sum = (~sum) & 0xffff
	sum = sum >> 8 | (sum << 8 & 0xff00)
	return sum

	
def usage():
	print "Usage:"
	print "\tsudo ./pyping destination [-c count] [-t second]"
	print "\tExample: pyping 192.168.0.1 -c 4 -t 0.5"
	print "\tExample: pyping www.google.com -t 2"
	exit()

	
if __name__=="__main__":
	count = 0		#default value
	timeout = 4
	interval = 0.1
	try:
		if len(sys.argv)==1:
			raise Exception
		dest = sys.argv[1]
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
	p = Ping(dest, count, timeout, interval)
	p.doping()