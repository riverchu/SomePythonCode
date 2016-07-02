# encoding UTF-8
import socket
import time

target_host = "10.8.172.4"
target_port = 9999

class Client():
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def work(self):
	#self.client.settimeout(10)
        self.client.connect((target_host,target_port))
	self.client.settimeout(10)
        print "[*]Connected!"
        
        try:
	    input = 'start!'
            #input = raw_input("[*]Input the message:")
        except KeyboardInterrupt: 
	    self.client.close()
            print "\n[-]Shutdown the connection!"
            return
        i=0
        while True:
            self.client.send(input)
            response = self.client.recv(4096)
            
            print response + "\t%d" % i
	    time.sleep(1)
                       
            try: 
                #input = raw_input("[*]Input the message:")
		input = "%d" % i
		#print "\t%d" % i
		i += 1
                if input == 'over':
                    break
            except KeyboardInterrupt: 
                break
	self.client.close()
        print "\n[-]Shutdown the connection!"

if __name__ == "__main__":
    socket = Client()
    socket.work()
