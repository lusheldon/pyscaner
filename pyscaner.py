#!/usr/bin/python
import sys, socket, time, struct, select, os, re, math

def pyscaner():
    target = []
    port = []
    if len(sys.argv)==3:
        target = sys.argv[1].split('/')
        port = sys.argv[2].split('-')
    else:
        print sys.argv
        usage("argv")
    # parse the host and mask
    
    host = target[0]
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, host):
        pass
    else:
        usage("ip not illeage")
    try:
        if len(target)==1:
            mask = 32
        elif len(target)==2:
            mask = int(target[1])
            if mask>0 and mask<33:
                pass
            else:
                usage("mask out bound")
        else:
            usage("need two arguments")
        #parse the startPort and endPort
        startPort = int(port[0])
        if startPort>0 and startPort<65535:
            pass
        else:
            usage("start port out of range")
        if len(port)==1:
            endPort = int(port[0])
        elif len(port)==2:
            endPort = int(port[1])
            if endPort>startPort and endPort<65535:
                pass
            else:
                raise "end port out of range"
        else:
            usage("wrong port arguments")
    except:
        raise "Wrong arguments"
    # startHost,endHost = parseHost(host, mask)
    # print startHost,endHost
    # if re.match(pattern, startHost):
        # pass
    # else:
        # usage("startHost parse error")
    scaner(host,mask,start,endPort)
def usage(str):
    print "Please input the correct parameters!"+str
    exit()
def scaner(host, mask, startPort, endPort):
    print "Scanning started!"
    ipDecRange=ipRange(ipToDec(host),mask)
    for ipDec in ipDecRange:
        # probe if the host alive
        ip=ipDectoStr(ipDec)
        if ipAlive(ip):
            for port in xrange(startPort, endPort):
                tcpConnect(ip,port)
def ipDectoStr(ipDec):
    ipList[0]=ipDec>>24
    ipList[1]=(ipDec-(ipList[0]<<24))>>16
    ipList[2]=(ipDec-(ipList[0]<<24)-(ipList[1]<<16))>>8
    ipList[3]=ipDec-(ipList[0]<<24)-(ipList[1]<<16)-ipList[2]<<8
    return '.'.join(ipList)
def ipAlive(ip):
    
    return True

def tcpConnect(ip,port):
    return True
#turn the host/mask into startHost and endHost
"""
def parseHost(host, mask):
    if mask==32:
        return (host,host)
    h=host.split('.')
    h_tmp=host.split('.')
    p=mask/8
    q=mask%8
    for n in range(128):
        if int(h[p])>=int(n*256/math.pow(2,q)) and int(h[p])<int((n+1)*256/math.pow(2,q)):
            flag = int(256/math.pow(2,q)*n)
            interval = int(256/math.pow(2,q))
            break
        else:
            pass
    if p<3:
        i=0
        while i<4:
            if i==p:
                h[i] = flag
                h_tmp[i] = flag+interval-1   
            elif i>p:
                h[i] = 0
                h_tmp[i] = 255
                h[3] = 1
                h_tmp[3] = 254
            else:
                pass
            i+=1
    else:
        h[3]=flag+1
        h_tmp[3]=flag+interval-2
    for i in range(4):
        h[i]=str(h[i])
        h_tmp[i]=str(h_tmp[i])
    return ('.'.join(h),'.'.join(h_tmp))
"""
def ipRange(ipDec,mask):
    startIpDec=(ipDec&((1<<mask)-1<<(32-mask)))
    endIpDec=(ipDec&((1<<mask)-1<<(32-mask)))+(1<<(32-mask))-1
    return xrange(startIpDec,endIpDec)
def ipToDec(ipstr):
    ipList=ipstr.split('.')
    return (ipList[0]<<24)+(ipList[1]<<16)+(ipList[2]<<8)+ipList
if __name__=="__main__":
    pyscaner()