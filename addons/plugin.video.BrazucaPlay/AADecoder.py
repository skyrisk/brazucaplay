# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for openload.io
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------
# Modified by Shani 
import re,urllib2

#from core import logger
#from core import scrapertools

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Connection', 'keep-alive']
]


class AADecoder(object):
    def __init__(self, aa_encoded_data):
        self.encoded_str = aa_encoded_data.replace('/*´∇｀*/','')

        self.b = ["(c^_^o)", "(ﾟΘﾟ)", "((o^_^o) - (ﾟΘﾟ))", "(o^_^o)",
                  "(ﾟｰﾟ)", "((ﾟｰﾟ) + (ﾟΘﾟ))", "((o^_^o) +(o^_^o))", "((ﾟｰﾟ) + (o^_^o))",
                  "((ﾟｰﾟ) + (ﾟｰﾟ))", "((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "(ﾟДﾟ) .ﾟωﾟﾉ", "(ﾟДﾟ) .ﾟΘﾟﾉ",
                  "(ﾟДﾟ) ['c']", "(ﾟДﾟ) .ﾟｰﾟﾉ", "(ﾟДﾟ) .ﾟДﾟﾉ", "(ﾟДﾟ) [ﾟΘﾟ]"]

    def is_aaencoded(self):
        idx = self.encoded_str.find("ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); ")
        if idx == -1:
            return False

        if self.encoded_str.find("(ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');", idx) == -1:
            return False

        return True

    def base_repr(self, number, base=2, padding=0):
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if base > len(digits):
            base = len(digits)

        num = abs(number)
        res = []
        while num:
            res.append(digits[num % base])
            num //= base
        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))

    def decode_char(self, enc_char, radix):
        end_char = "+ "
        str_char = ""
        while enc_char != '':
            found = False
            for i in range(len(self.b)):
                #print self.b[i],enc_char.find(self.b[i])
                if enc_char.find(self.b[i]) == 0:
                    str_char += self.base_repr(i, radix)
                    enc_char = enc_char[len(self.b[i]):]
                    found = True
                    break

            #print 'found',found,enc_char
            if not found:
                #enc_char=enc_char.replace('(ﾟΘﾟ)','1').replace('(ﾟｰﾟ)','4').replace('(c^_^o)','0').replace('(o^_^o)','3')
                #print 'enc_char',enc_char
                startpos=0
                findClose=True
                balance=1
                result=[]
                if enc_char.startswith('('):
                    l=0
                    
                    for t in enc_char[1:]:
                        l+=1
                        #print 'looping',findClose,startpos,t,balance
                        if findClose and t==')':
                            balance-=1;
                            if balance==0:
                                result+=[enc_char[startpos:l+1]]
                                findClose=False
                                continue
                        elif not findClose and t=='(':
                            startpos=l
                            findClose=True
                            balance=1
                            continue
                        elif t=='(':
                            balance+=1
                 
                            
                            
                                
                
                #print 'normal',enc_char
                #if enc_char.startswith('((') or enc_char.startswith('(-(') or enc_char.startswith('(+('):
                #    rr='(\(.*?\)\))\+'
                #else:
                #    rr="(\(.*?\))\+"
                #result = re.findall("(\(.*?\))\+", enc_char)
                #print 'res',result
               # result = re.search("\((.+?)\)\+ ?", enc_char, re.DOTALL)
                if result is None or len(result)==0:
                    return ""
                else:
                    #print 'here', enc_char
                    #enc_char = enc_char[len(result.group(1)) + 2:]
                    #print 'here',repr(enc_char)
                    #print 'decodeme',result.group(1)
                    #value = self.decode_digit(result.group(1), radix)
                    for r in result:
                        value = self.decode_digit(r, radix)
                        #print 'va',value
                        if value == "":
                            return ""
                        else:
                            
                            str_char += value
                    return str_char

            enc_char = enc_char[len(end_char):]

        return str_char
    def parseJSString(self,s):
        try:
            #print s
            offset=1 if s[0]=='+' else 0
            tmp=(s.replace('!+[]','1').replace('!![]','1').replace('[]','0'))#.replace('(','str(')[offset:])
            val = int(eval(tmp))
            return val
        except:
            pass
        
    def decode_digit(self, enc_int, radix):
        enc_int=enc_int.replace('(ﾟΘﾟ)','1').replace('(ﾟｰﾟ)','4').replace('(c^_^o)','0').replace('(o^_^o)','3')  

        rr='(\(.+?\)\))\+'
        rerr=enc_int.split('))+')#re.findall(rr,enc_int)
        v=""
        #print rerr
        for c in rerr:
            if len(c)>0:
                #print 'v',c
                if c.strip().endswith('+'):
                    c=c.strip()[:-1]
                #print 'v',c
                startbrackets=len(c)-len(c.replace('(',''))
                endbrackets=len(c)-len(c.replace(')',''))
                if startbrackets>endbrackets:
                    c+=')'*startbrackets-endbrackets
                if '[' in c :
                    v+=str(self.parseJSString(c))
                else:
                    v+=str(eval(c))
        return v
            
        # mode 0=+, 1=-
        mode = 0
        value = 0

        while enc_int != '':
            found = False
            for i in range(len(self.b)):
                if enc_int.find(self.b[i]) == 0:
                    if mode == 0:
                        value += i
                    else:
                        value -= i
                    enc_int = enc_int[len(self.b[i]):]
                    found = True
                    break

            if not found:
                return ""

            enc_int = re.sub('^\s+|\s+$', '', enc_int)
            if enc_int.find("+") == 0:
                mode = 0
            else:
                mode = 1

            enc_int = enc_int[1:]
            enc_int = re.sub('^\s+|\s+$', '', enc_int)

        return self.base_repr(value, radix)

    def decode(self):
        self.encoded_str = re.sub('^\s+|\s+$', '', self.encoded_str)

        # get data
        pattern = (r"\(ﾟДﾟ\)\[ﾟoﾟ\]\+ (.+?)\(ﾟДﾟ\)\[ﾟoﾟ\]\)")
        result = re.search(pattern, self.encoded_str, re.DOTALL)
        if result is None:
            print "AADecoder: data not found"
            return False

        data = result.group(1)

        # hex decode string
        begin_char = "(ﾟДﾟ)[ﾟεﾟ]+"
        alt_char = "(oﾟｰﾟo)+ "

        out = ''
        #print data
        while data != '':
            # Check new char
            if data.find(begin_char) != 0:
                print "AADecoder: data not found"
                return False

            data = data[len(begin_char):]

            # Find encoded char
            enc_char = ""
            if data.find(begin_char) == -1:
                enc_char = data
                data = ""
            else:
                enc_char = data[:data.find(begin_char)]
                data = data[len(enc_char):]

            
            radix = 8
            # Detect radix 16 for utf8 char
            if enc_char.find(alt_char) == 0:
                enc_char = enc_char[len(alt_char):]
                radix = 16

            #print repr(enc_char),radix
            #print enc_char.replace('(ﾟΘﾟ)','1').replace('(ﾟｰﾟ)','4').replace('(c^_^o)','0').replace('(o^_^o)','3')
            
            #print 'The CHAR',enc_char,radix
            str_char = self.decode_char(enc_char, radix)
            
            if str_char == "":
                print "no match :  "
                print  data + "\nout = " + out + "\n"
                return False
            #print 'sofar',str_char,radix,out
            
            out += chr(int(str_char, radix))
            #print 'sfar',chr(int(str_char, radix)),out

        if out == "":
            print "no match : " + data
            return False

        return out


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


