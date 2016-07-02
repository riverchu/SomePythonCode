# encoding: UTF-8
import os
import socket
import struct
import threading
import time
from ctypes import *
from netaddr import IPNetwork,IPAddress

#监听的主机
host   = "192.168.229.128"

#扫描的目标子网
subnet = "192.168.229.129"

magic_message = "PYTHONRULES!"

def udp_sender(subnet,magic_message):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    for ip in IPNetwork(subnet):
        
        try:
            sender.sendto(magic_message,("%s" % ip,65212))
        except:
            pass

#ip头定义
class IP(Structure):
    _fields_ = [
        ("ihl",         c_ubyte,4),
        ("version",     c_ubyte,4),
        ("tos",         c_ubyte),
        ("len",         c_ushort),
        ("id",          c_ushort),
        ("offset",      c_ushort),
        ("ttl",         c_ubyte),
        ("protocol_num",c_ubyte),
        ("sum",         c_ushort),
        #("src",         c_ulong),x86
        #("dst",         c_ulong)x86
        ("src",         c_uint32),
        ("dst",         c_uint32)
    ]
    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self,socket_buffer=None):
        #协议字段和名称进行转换
        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"}
        
        #可读性更强的IP地址
        #self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))x86
        #self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))x86
        self.src_address = socket.inet_ntoa(struct.pack("@I",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I",self.dst))       
        
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

class ICMP(Structure):
    
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
    ]
    def __new__(self,socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self,socket_buffer):
        pass
            
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
            
sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
        
sniffer.bind((host,0))
        
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
        
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)    

t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()

#print sniffer.recvfrom(65565)
try:
    while True:
        
        #读取数据包
        #raw_buffer = sniffer.recvfrom(65565)[0] x86
        raw_buffer = sniffer.recvfrom(65565)[0]
        
        #将缓冲区的ip头按前20个字节进行解析
        ip_header = IP(raw_buffer[:20])#x86
        
        print "Protocol: %s %s -> %s" %(ip_header.protocol,ip_header.src_address,ip_header.dst_address)
        
        #如果为ICMP 进行解构
        if ip_header.protocol == "ICMP":
             
             offset = ip_header.ihl*4
             buf = raw_buffer[offset:offset+sizeof(ICMP)]
             
             icmp_header = ICMP(buf)
             
             print "ICMP -> Type: %d Code: %d" % (icmp_header.type,icmp_header.code)
             
             if icmp_header.code == 3 and icmp_header.type == 3:
                 
                 #确认主机在目标子网列表中
                 if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                     #确认发送的magic_message
                     if raw_buffer[len(raw_buffer)-len(magic_message):] == magic_message:
                         print "Host Up: %s" % ip_header.src_address
        
except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)        
        
        
        