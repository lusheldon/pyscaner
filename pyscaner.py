#!/usr/bin/python
import sys, socket, time, struct, select, os, re, math
import pyping

def pyscaner():
    target = []
    port = []
    if len(sys.argv) == 3:
        target = sys.argv[1].split('/')
        port = sys.argv[2].split('-')
    else:
        print sys.argv
        usage("argv")
    # parse the host and mask

    host = target[0]
    pattern = (r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
               r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")
    if re.match(pattern, host):
        pass
    else:
        usage("ip not illegal")
    try:
        if len(target) == 1:
            mask = 32
        elif len(target) == 2:
            mask = int(target[1])
            if 0 < mask < 33:
                pass
            else:
                usage("mask out bound")
        else:
            usage("need two arguments")
        # parse the start_port and end_port
        start_port = int(port[0])
        if 0 < start_port < 65535:
            pass
        else:
            usage("start port out of range")
        if len(port) == 1:
            end_port = int(port[0])
        elif len(port) == 2:
            end_port = int(port[1])
            if start_port < end_port < 65535:
                pass
            else:
                usage("end port out of range")
        else:
            usage("wrong port arguments")
    except:
        raise TypeError("Wrong arguments")
        # startHost,endHost = parseHost(host, mask)
        # print startHost,endHost
        # if re.match(pattern, startHost):
        # pass
        # else:
        # usage("startHost parse error")
    scaner(host, mask, start_port, end_port)


def usage(msg):
    print "Please input the correct parameters!" + msg
    exit()


def scaner(host, mask, start_port, end_port):
    print "Scanning started!"
    ip_dec = ip_to_dec(host)
    start_ip_dec = (ip_dec & ((1 << mask) - 1 << (32 - mask))) + 1
    end_ip_dec = (ip_dec & ((1 << mask) - 1 << (32 - mask))) + (1 << (32 - mask)) - 1
    # To avoid overflowerror int too large to convert long
    diff_value = end_ip_dec - start_ip_dec
    ip_dec_range = xrange(0, diff_value)
    for ipDec in ip_dec_range:
        # probe if the host alive
        ip = ip_dec_to_str(ipDec+start_ip_dec)
        # print ipDec,ip
        if pyping.probe(ip):
            for port in xrange(start_port, end_port+1):
                tcp_connect(ip, port)
        else:
            pass# print ip, "is not alive, skipped!"
		

def ip_dec_to_str(ip_dec):
    ipp1 = ip_dec >> 24
    ipp2 = (ip_dec - (ipp1 << 24)) >> 16
    ipp3 = (ip_dec - (ipp1 << 24) - (ipp2 << 16)) >> 8
    ipp4 = ip_dec - (ipp1 << 24) - (ipp2 << 16) - (ipp3 << 8)
    ipp = [ipp1 % 256 + ipp1 / 256, ipp2 % 256 + ipp2 / 256, ipp3 % 256 + ipp3 / 256, ipp4 % 256 + ipp4 / 256]
    ipp = [str(i) for i in ipp]
    return '.'.join(ipp)


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


# turn the host/mask into startHost and endHost
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
def ip_to_dec(ip):
    ip_array = ip.split('.')
    ip_array = [int(x) for x in ip_array]
    return (ip_array[0] << 24) + (ip_array[1] << 16) + (ip_array[2] << 8) + ip_array[3]


if __name__ == "__main__":
    pyscaner()
