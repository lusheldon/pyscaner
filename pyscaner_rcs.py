#!/usr/bin/python
import sys, re

def usage():


def isIp(str):
	pattern = (r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
			r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")
	return re.match(pattern, host)


def argpase():
	target = []
	port = [20, 21, 22, 23, 25, 53, 80, 110, 119, 139, 161, 162, 443]
	if 1<len(sys.argv)<4:
		if '/' in sys.argv[1]:
			target = sys.argv[1].split('/')
		elif '-' in sys.argv[1]:
			target = sys.argv[1].split('-')
		else：
			target = sys.argv[1]
		if len(sys.argv)==3:
			port = sys.argv[2].split('-')
	else:
		usage():
	if isIp(target[0]) and 1<port[0]<65535:
		parseHost(target)
		parsePort(port)
	else:
		usage()

		
def parseHost(host):
	if isIp(host[0]):
	else:
		usage()

if __name__=="__main__":
	argpase()