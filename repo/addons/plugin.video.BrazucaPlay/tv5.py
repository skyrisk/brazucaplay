
import base64
import zlib, urllib,urllib2,re
key=base64.b64decode("ZXQgb3VhaSBtZWMh")
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;


def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
#    print ord(decoded_data[0])
    return zlib.decompress( decoded_data , 15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string =zlibbed_str## zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )
    
def decode(param1, param2):
    param1dec=decode_base64_and_inflate(param1)
    _loc3_ = bytearray()
    _loc3_.extend(param1dec)
    _loc4_ = 0;
    _loc5_ = len(param1dec);
    _loc6_ = 0;
    while _loc6_ < _loc5_:
        _loc3_[_loc6_] = _loc3_[_loc6_] ^ ord(param2[_loc4_]);
        _loc4_+=1;
        if(_loc4_ >= len(param2)):
            _loc4_ = 0;
        _loc6_+=1;
    return _loc3_
def encode(param1, param2):
    param1dec=param1
    _loc3_ = bytearray()
    _loc3_.extend(param1dec)
    _loc4_ = 0;
    _loc5_ = len(param1dec);
    _loc6_ = 0;
    while _loc6_ < _loc5_:
        _loc3_[_loc6_] = _loc3_[_loc6_] ^ ord(param2[_loc4_]);
        _loc4_+=1;
        if(_loc4_ >= len(param2)):
            _loc4_ = 0;
        _loc6_+=1;
    return  deflate_and_base64_encode(_loc3_.decode("utf-8"))
    return _loc3_  

def extractUrl(uid):    
#enc="eNrjYnGVFRFl8GeOYHERtPTnZuDlYZPgYZdhkfXlCgjR9+XhZAlmCBTVlBRhYI1QFhAMAbIFBKMkPAJURcOcxWNcwwEd4gnn" 
#    eJzjYnGVFRFl8GeOYHERtPTnZuDlYZPgYZdhkfXlCgjR9+XhZAlmCBTVlBRhYI1QFhAMAbIFBKMkPAJURcOcxWNcwwEd4gnn   

    str="operation=getPlaylist&uid=%s"%urllib.quote_plus(uid)
    str=encode(str,key)
    s=getUrl("http://www.tv5mondeplusafrique.com/html/servicesV2/getPlaylist.xml?BulkLoaderNoCache=2_2&",post=str)
    s=decode(s,key)
    print "returned", repr(s.decode("unicode-escape"))
    from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
    xmlobj= BeautifulSOAP(s.decode("unicode-escape"), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    
    vurl=xmlobj("video")[0];
#    print vurl
    su=vurl("secureurl")[0].string
    su=re.sub('[\[CDATA\]]', '', su)
    #print su
#    print 'yyyyyyyyyyyy',vurl
    if 'manifest.f4m?' in su:
        su='plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(su)
    return su
#print   extractUrl("aime_malgre_lui_s01_ep42_4377314")  
#d1= decode(enc,key)
#print d1
#d2=encode(d1,key)
#print d2
#print d1==d2
#print 1/0
#print decode(enc, key)

#print decode("eNrjYnGVFRFl8GeOYHERVPHh4+FlCJZ0FvNg9HRkk2DxEdXmYPJlYnP1clBnDWVxCEsXcxEEsnkC4mLdRJQdhCOcgiLFAFb/C4g=",key)    
#print decode("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",key)    
 