# encoding: UTF-8

import re
import urllib  
import urllib2
import cookielib
from time import clock

cookie = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


#需要POST的数据#
postdata=urllib.urlencode({  
    'DDDDD'     :2015213361,  
    'upass'     :263217,
    '0MKKey'    :'\314\341\275\273'
    
})
#自定义一个请求#
req = urllib2.Request(  
    url = 'http://10.3.8.211',
    data = postdata
)

#访问该链接#
result = opener.open(req)


#打印返回的内容
#print result.read()

m = re.search(r'Msg', str(result.read()))
if not m:
    string= 'Success'
    print string

