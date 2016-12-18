#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Sheldon'
import sys, re, threading, socket, pyping

def usage(str):
	print str + "\n"
	print "Usage:"
	print "\tsudo ./pyscaner.py target [port]"
	print "\tExample: sudo ./pyscaner.py 192.168.0.1/24 22-80"
	print "\tExample: sudo ./pyscaner.py 192.168.0.1 22"
	print "\tExample: sudo ./pyscaner.py 192.168.0.1"
	exit()

def isIp(str):
	pattern = (r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
               r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")
	return re.match(pattern, str) # return True if it is a unicast address


def argpase():
	target = []
	port = [20, 21, 22, 23, 25, 53, 80, 110, 119, 139, 161, 162, 443, 3389, 8080]
	if len(sys.argv)==3:
		port = sys.argv[2].split('-')
	if 1<len(sys.argv)<4:
		if '/' in sys.argv[1]:
			target = sys.argv[1].split('/')
		elif '-' in sys.argv[1]:
			target = sys.argv[1].split('-')
		else:
			target.append(sys.argv[1])
	else:
		usage("Only 2 or 3 parameters are acceptable!")
	if isIp(target[0]) and 1<int(port[0])<65535:
		target = parseHost(target)
		port = parsePort(port)
	else:
		usage("Port range should be 1~65535")
	do_scan(target, port)

def ip_to_dec(ip):
	ip_array = ip.split('.')
	ip_array = [int(x) for x in ip_array]
	return (ip_array[0] << 24) + (ip_array[1] << 16) + (ip_array[2] << 8) + ip_array[3]


def ip_dec_to_str(ip_dec):
    ipp1 = ip_dec >> 24
    ipp2 = (ip_dec - (ipp1 << 24)) >> 16
    ipp3 = (ip_dec - (ipp1 << 24) - (ipp2 << 16)) >> 8
    ipp4 = ip_dec - (ipp1 << 24) - (ipp2 << 16) - (ipp3 << 8)
    ipp = [ipp1 % 256 + ipp1 / 256, ipp2 % 256 + ipp2 / 256, ipp3 % 256 + ipp3 / 256, ipp4 % 256 + ipp4 / 256]
    ipp = [str(i) for i in ipp]
    return '.'.join(ipp)


def parseHost(target):
	'''
	if -1 contained, it is a range
	elif 0 contained, it is illeage
	else it is a list
	'''
	try:
		if len(target)==2:
			if isIp(target[1]):
				target = map(lambda ip: ip_to_dec(ip), target)
				return [-1,target[0],target[1]+1]
			elif 0<int(target[1])<32:
				ip_dec = ip_to_dec(target[0])
				mask = int(target[1])
				start_ip_dec = (ip_dec & ((1 << mask) - 1 << (32 - mask))) + 1
				end_ip_dec = (ip_dec & ((1 << mask) - 1 << (32 - mask))) + (1 << (32 - mask)) - 1
				return [-1, start_ip_dec, end_ip_dec]
		elif len(target)==1:
			return [ip_to_dec(target[0])]
		else:
			raise ValueError
	except:
		usage("Target range is wrong!")

def parsePort(port):
	'''
	if -1 contained, it is a range
	elif 0 contained, it is illeage
	else it is a list
	'''
	try:
		if len(port)==15:
			return port
		elif len(port)==2:
			start_port = int(port[0])
			end_port = int(port[1])+1
			if start_port<end_port<65535:
				return [-1, start_port, end_port]
			else:
				raise ValueError
		else:
			port = map(lambda str: int(str) if 0<int(str)<65535 else 0, port)
			assert 0 not in port
			return port
	except:	
		usage("Port range is wrong!")
	

# class Scaner(threading.Thread):


def do_scan(target, port):
	if len(target)==3 and target[0]==-1:
		target_range = xrange(target[1],target[2])
	else:
		target_range = target
	if len(port)==3 and port[0]==-1:
		port_range = xrange(port[1], port[2])
	else:
		port_range = port
	ping = pyping.Ping('')
	for ip_dec in target_range:
		# print ip_dec
		ip = ip_dec_to_str(ip_dec)
		ping.dest = ip
		# if ping.probe():
		for p in port_range:
			tcp_connect(ip, p)
	
def tcp_connect(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	#sock.setsockopt(socket.SOL_SOCKet, socket.SO_REUSEPORT, 1)
	# print "try to connect"
	try:
		sock.connect((ip,port))
		print "detected opened port", ip, port
		return True
	except socket.error, e:
		# print "Error+: ", e
		return False
	finally:
		sock.close()			

	
if __name__=="__main__":
	argpase()