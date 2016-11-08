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
                usage("end port out of range")
        else:
            usage("wrong port arguments")
    except:
        usage("Wrong arguments")
    startHost,endHost = parseHost(host, mask)
    print startHost,endHost
    if re.match(pattern, startHost):
        pass
    else:
        usage("startHost parse error")
    scaner(startHost, endHost, startPort, endPort)
def usage(str):
    print "Please input the correct parameters!"+str
    exit()
def scaner(startHost, endHost, startPort, endPort):
    print "Scanning started!"
    

#turn the host/mask into startHost and endHost
def parseHost(host, mask):
    if mask==32:
        return (host,host)
    h=host.split('.')
    h_tmp=h
    p=mask/8
    q=mask%8
    print h
    print p,q,h[p-1]
    for n in range(128):
        if int(h[p-1])>=int(n*256/math.pow(2,q)) and int(h[p-1])<int((n+1)*256/math.pow(2,q)):
            flag = int(256/math.pow(2,q)*n)
            interval = int(256/math.pow(2,q))
            break
        else:
            pass
    print flag, interval
    if p<3:
        for i in range(3):
            if i<p-1:
                pass
            elif i==p-1:
                h[i] = flag
                h_tmp[i] = flag+interval-1
                
            else:
                h[i] = 0
                h_tmp[i] = 0
                h[3] = 1
                h_tmp[3] = 254
    else:
        h_tmp=h
        h[3]=flag+1
        h_tmp[3]=flag+interval-1
    print h,h_tmp
    for i in range(4):
        h[i]=str(h[i])
        h_tmp[i]=str(h_tmp[i])
    return ('.'.join(h),'.'.join(h_tmp))
    
if __name__=="__main__":
    pyscaner()