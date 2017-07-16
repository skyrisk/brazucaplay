## ONLY FOR NOOBS :D
##CONVERSION OF following encryption by shani into python
## only decryption function is implemented
'''
 * jQuery JavaScript Library v1.4.2
 * http://jquery.com/
 *
 * Copyright 2010, John Resig
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * Includes Sizzle.js
 * http://sizzlejs.com/
 * Copyright 2010, The Dojo Foundation
 * Released under the MIT, BSD, and GPL Licenses.
 *
 * Date: Sat Feb 13 22:33:48 2010 -0500
 '''

import urllib
import base64
import re,urllib2,cookielib


def decode(r):
    e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    r = r.replace("\n", "");
    f = []
    c = [0,0,0,0]
    t = [0,0,0];
#    print 'rrrrrrrrrrrrrrrrrrrrrrrr',r
    for n  in range(0 ,len(r),4):
        c[0]=-1
        try:
            c[0] = e.index(r[n]);
        except:pass
        c[1]=-1
        try:
            c[1] = e.index(r[n + 1])
        except:pass
        c[2]=-1
        try:
            c[2] = e.index(r[n + 2]);
        except:pass
        c[3]=-1
        try:
            c[3] = e.index(r[n + 3])
        except:pass
        t[0] = c[0] << 2 | c[1] >> 4
        t[1] = (15 & c[1]) << 4 | c[2] >> 2
        t[2] = (3 & c[2]) << 6 | c[3]
        f+=[t[0], t[1], t[2]];
#    print f
#    print f[0:10]
    return f[0: len(f) - (len(f) % 16)]

'''
def fun_e:
    return unescape(encodeURIComponent(e))
            } catch (r) {
                throw "Error utf"
            }
'''       
def func_u(e):
    c = [];
    #if decode:
#    print 'basssssssssssssssssssssss', base64.decode(e)
#    return 
#    e= urllib.unquote(base64.decode(e))
    for n in range(0, len(e)):
        c.append(ord(e[n]));
    return c

def fun_A(e, r):
    n=0;
    f = [None]*(len(e) / r);
    for n in range(0, len(e),r):
        f[n / r] = int(e[n:n+r], 16);
    return f    

    
'''L inner functions 
'''
def func_L_r(e, r):
    return e << r | e >> 32 - r ##change>>>


def func_L_n(e, r):
    c = 2147483648 & e
    t = 2147483648 & r
    n = 1073741824 & e 
    f = 1073741824 & r 
    a = (1073741823 & e) + (1073741823 & r)
    return  (2147483648 ^ a ^ c ^ t) if n & f else ( (3221225472 ^ a ^ c ^ t if 1073741824 & a else 1073741824 ^ a ^ c ^ t ) if n | f else a ^ c ^ t)

    
def func_L_f(e, r, n):
    return e & r | ~e & n


def func_L_c(e, r, n):
    return e & n | r & ~n

def func_L_t(e, r, n):
    return e ^ r ^ n
            
def func_L_a(e, r, n):
    return r ^ (e | ~n)

def func_L_o(e, c, t, a, o, d, u):
    e = func_L_n(e, func_L_n(func_L_n(func_L_f(c, t, a), o), u))
    return func_L_n(func_L_r(e, d), c)


def func_L_d(e, f, t, a, o, d, u):
    e = func_L_n(e, func_L_n(func_L_n(func_L_c(f, t, a), o), u))
    return  func_L_n(func_L_r(e, d), f)
            

def func_L_u(e, f, c, a, o, d, u):
    e = func_L_n(e, func_L_n(func_L_n(func_L_t(f, c, a), o), u))
    return func_L_n(func_L_r(e, d), f)

def func_L_i(e, f, c, t, o, d, u):
    e = func_L_n(e, func_L_n(func_L_n(func_L_a(f, c, t), o), u))
    return func_L_n(func_L_r(e, d), f)

def func_L_b(e):
 
    n = len(e)
    f = n + 8
    c = (f - f % 64) / 64
    t = 16 * (c + 1)
    a = [0]*(n+1)
    o = 0; d = 0
    
#    for (var r, n = e.length, f = n + 8, c = (f - f % 64) / 64, t = 16 * (c + 1), a = [], o = 0, d = 0; n > d;) r = (d - d % 4) / 4, o = 8 * (d % 4), 
    for d in range(0,n):
        r = (d - d % 4) / 4; 
        o = 8 * (d % 4); 
        #print a[r]
        #print e[d]
        a[r] = a[r] | e[d] << o

    d+=1
#    print a, d,n
    r = (d - d % 4) / 4
    o = 8 * (d % 4)
    a[r] = a[r] | 128 << o
    a[t - 2] = n << 3
#    print 'tttttttttttttttttt',t
#    print 'len a',len(a)
    try:
        a[t - 1] = n >> 29# >>> removed
    except: pass
    return a


def func_L_h(e):
    f = [];
    for n in range(0,4):
        r = 255 & e >> 8 * n #>>> removed
        f.append(r)
    return f

 
def func_L(e):
    l=0
    v=0
    S = [];
    m = fun_A("67452301efcdab8998badcfe10325476d76aa478e8c7b756242070dbc1bdceeef57c0faf4787c62aa8304613fd469501698098d88b44f7afffff5bb1895cd7be6b901122fd987193a679438e49b40821f61e2562c040b340265e5a51e9b6c7aad62f105d02441453d8a1e681e7d3fbc821e1cde6c33707d6f4d50d87455a14eda9e3e905fcefa3f8676f02d98d2a4c8afffa39428771f6816d9d6122fde5380ca4beea444bdecfa9f6bb4b60bebfbc70289b7ec6eaa127fad4ef308504881d05d9d4d039e6db99e51fa27cf8c4ac5665f4292244432aff97ab9423a7fc93a039655b59c38f0ccc92ffeff47d85845dd16fa87e4ffe2ce6e0a30143144e0811a1f7537e82bd3af2352ad7d2bbeb86d391", 8);
#    print m
#    print 'eeeeeeeeeeeeeeeeeeeeee',e
    S = func_L_b(e); 
#    print 'S is     ',S
    
    y = m[0]; k = m[1]; M = m[2]; x = m[3]
    for l in range(0, len(S),16):
        v = y; s = k; p = M; g = x;
        y = func_L_o(y, k, M, x, S[l + 0], 7, m[4])
        x = func_L_o(x, y, k, M, S[l + 1], 12, m[5])
        M = func_L_o(M, x, y, k, S[l + 2], 17, m[6])
        k = func_L_o(k, M, x, y, S[l + 3], 22, m[7])
        y = func_L_o(y, k, M, x, S[l + 4], 7, m[8])
        x = func_L_o(x, y, k, M, S[l + 5], 12, m[9])
        M = func_L_o(M, x, y, k, S[l + 6], 17, m[10])
        k = func_L_o(k, M, x, y, S[l + 7], 22, m[11])
        y = func_L_o(y, k, M, x, S[l + 8], 7, m[12])
        x = func_L_o(x, y, k, M, S[l + 9], 12, m[13])
        M = func_L_o(M, x, y, k, S[l + 10], 17, m[14])
        k = func_L_o(k, M, x, y, S[l + 11], 22, m[15])
        y = func_L_o(y, k, M, x, S[l + 12], 7, m[16])
        x = func_L_o(x, y, k, M, S[l + 13], 12, m[17])
        M = func_L_o(M, x, y, k, S[l + 14], 17, m[18])
        k = func_L_o(k, M, x, y, S[l + 15], 22, m[19])
        y = func_L_d(y, k, M, x, S[l + 1], 5, m[20])
        x = func_L_d(x, y, k, M, S[l + 6], 9, m[21])
        M = func_L_d(M, x, y, k, S[l + 11], 14, m[22])
        k = func_L_d(k, M, x, y, S[l + 0], 20, m[23])
        y = func_L_d(y, k, M, x, S[l + 5], 5, m[24])
        x = func_L_d(x, y, k, M, S[l + 10], 9, m[25])
        M = func_L_d(M, x, y, k, S[l + 15], 14, m[26])
        k = func_L_d(k, M, x, y, S[l + 4], 20, m[27])
        y = func_L_d(y, k, M, x, S[l + 9], 5, m[28])
        x = func_L_d(x, y, k, M, S[l + 14], 9, m[29])
        M = func_L_d(M, x, y, k, S[l + 3], 14, m[30])
        k = func_L_d(k, M, x, y, S[l + 8], 20, m[31])
        y = func_L_d(y, k, M, x, S[l + 13], 5, m[32])
        x = func_L_d(x, y, k, M, S[l + 2], 9, m[33])
        M = func_L_d(M, x, y, k, S[l + 7], 14, m[34])
        k = func_L_d(k, M, x, y, S[l + 12], 20, m[35])
        y = func_L_u(y, k, M, x, S[l + 5], 4, m[36])
        x = func_L_u(x, y, k, M, S[l + 8], 11, m[37])
        M = func_L_u(M, x, y, k, S[l + 11], 16, m[38])
        k = func_L_u(k, M, x, y, S[l + 14], 23, m[39])
        y = func_L_u(y, k, M, x, S[l + 1], 4, m[40])
        x = func_L_u(x, y, k, M, S[l + 4], 11, m[41])
        M = func_L_u(M, x, y, k, S[l + 7], 16, m[42])
        k = func_L_u(k, M, x, y, S[l + 10], 23, m[43])
        y = func_L_u(y, k, M, x, S[l + 13], 4, m[44])
        x = func_L_u(x, y, k, M, S[l + 0], 11, m[45])
        M = func_L_u(M, x, y, k, S[l + 3], 16, m[46])
        k = func_L_u(k, M, x, y, S[l + 6], 23, m[47])
        y = func_L_u(y, k, M, x, S[l + 9], 4, m[48])
        x = func_L_u(x, y, k, M, S[l + 12], 11, m[49])
        M = func_L_u(M, x, y, k, S[l + 15], 16, m[50])
        k = func_L_u(k, M, x, y, S[l + 2], 23, m[51])
        y = func_L_i(y, k, M, x, S[l + 0], 6, m[52])
        x = func_L_i(x, y, k, M, S[l + 7], 10, m[53])
        M = func_L_i(M, x, y, k, S[l + 14], 15, m[54])
        k = func_L_i(k, M, x, y, S[l + 5], 21, m[55])
        y = func_L_i(y, k, M, x, S[l + 12], 6, m[56])
        x = func_L_i(x, y, k, M, S[l + 3], 10, m[57])
        M = func_L_i(M, x, y, k, S[l + 10], 15, m[58])
        k = func_L_i(k, M, x, y, S[l + 1], 21, m[59])
        y = func_L_i(y, k, M, x, S[l + 8], 6, m[60])
        x = func_L_i(x, y, k, M, S[l + 15], 10, m[61])
        M = func_L_i(M, x, y, k, S[l + 6], 15, m[62])
        k = func_L_i(k, M, x, y, S[l + 13], 21, m[63])
        y = func_L_i(y, k, M, x, S[l + 4], 6, m[64])
        x = func_L_i(x, y, k, M, S[l + 11], 10, m[65])
        M = func_L_i(M, x, y, k, S[l + 2], 15, m[66])
        k = func_L_i(k, M, x, y, S[l + 9], 21, m[67])
        y = func_L_n(y, v)
        k = func_L_n(k, s)
        M = func_L_n(M, p)
        x = func_L_n(x, g)
#        print 'y is ' ,y,func_L_h(y)
        return func_L_h(y)+func_L_h(k)+ func_L_h(M)+func_L_h(x)
            

def func_h(n, f):
    c=0
    e = 14
    r = 8
    t = 3 if e >= 12 else 2
    a = []
    o = []
    d = [None]*t
    u = [],
    i = n+ f;
#    print 'n is',n
#    print 'f is',f
#    print 'i is',i
#    print 'func_L(i)'
    #print func_L(i)
    #return '',''
    d[0] = func_L(i)
    
#    print 'dddddddddddddddd',d
    u = d[0] 
#    print 'uuuuuuuuuuuuuuuu',u
    #print u
    for c  in range(1,t):
        d[c] = func_L( d[c - 1]+i ) 
        u+=(d[c])
#    print u
    a = u[0: 4 * r]
    o = u[4 * r: 4 * r + 16]
    return a,o

def decrypt(val,key):    
    f= decode(val);
    c=f[8:16]
    k=func_u(key);
    
    a,o= func_h(k, c)
#    print 'aaaaaaaaaaaaaaaaa is ',a
#    print 'oooooooooooooooo is ',o
    
    #print c
    f=f[16:]
    key=a
    iv=o
 #   print len(key)
    key2=""
    for k in range(0,len(key)):
        key2+=chr(key[k])
    iv2=""
    for k in range(0,len(iv)):
        iv2+=chr(iv[k])
    f2=""    
    for k in range(0,len(f)):
        f2+=chr(f[k])
        
    

    import pyaes
    decryptor = pyaes.new(key2, pyaes.MODE_CBC, IV=iv2)
    return decryptor.decrypt(f).replace('\x00', '')


def getCaptchaUrl(page_data):
    patt='jQuery.dec\("(.*?)", "(.*?)"'
    print page_data
    txt,key=re.findall(patt,page_data)[0]
    decText=decrypt(txt,key);
    print 'first dec',decText
    iloop=0

    while 'jQuery.dec(' in decText  and iloop<5:
        iloop+=1
        txt,key=re.findall(patt,decText)[0]
    #    print 'txt\n',txt
    #    print 'key\n',key
        decText=decrypt(txt,key);
    print 'final dec',decText   
    img_pat='<img src="(.*?)"'
    img_url=re.findall(img_pat,decText)[0]
    if not img_url.startswith('http'):
        img_url='http://oneplay.tv/embed/'+img_url
    print 'catcha url',img_url
    return img_url
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None, returnResponse=False, noredirect=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
#    opener = urllib2.install_opener(opener)
    
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    if returnResponse: return response
    link=response.read()
    response.close()
    return link;
    
def decrypt_oneplaypage(page_url, cookieJar):
    if page_url.startswith("http"):
        page_data= getUrl(page_url,cookieJar)
    else:
        page_data=page_url
#    print page_data
    patt='\$\(document\)\[(.*?\])'
    myvar=''
    var_dec='myvar='+re.findall(patt,page_data)[0]
#    print var_dec
    exec(var_dec)
#    print myvar
    data='';key=''
    for i in range(len(myvar)):
        if len(myvar[i])>100: data=myvar[i];#
        if len(myvar[i])==10: key=myvar[i]
        
   # print myvar[1],myvar[3]
    s=decrypt (data,key)
    print s
    return s

#print decrypt_oneplaypage('http://oneplay.tv/embed/?i=94&n=VH1&w=100%&h=480' ,None)
#print decrypt("U2FsdGVkX19zHnMuwv6Wdv8ap6pV/ZMTPd5y2B0B3WZ3N1YDS+9e3aqW/6vue+AjizICMLtuQJ2JUgYygfhQ4gRvcukV444ns3HvnpYRQ2Oy3Bse5k+NgRDAorrdZpLMQjyZIfdIhJVdIi0PeGTqGcwxAfGdaFYLc6aQNctw/6wFnCfF4VYkjEK+DK/3D0tyln8k+VmsQXZ1B4+W7sWYTsHhLUwZgErXwpfRrdJ2aWh8P+/u7vroK1Gj6DADKePq/f4dSEDZL41lSpjy21h0RIZznrk9mONDfAEpuvKxyLtXIlVVnikHXSU4jK26YP7aYIei6SciPrhU3XHmxerF95lGUWyw7tMRMxwk8kZ+6CqrpiCjjfjCXvYW68VlBOdBYKXB00HxZiNFpcNwKJ5NjUmY2SgzPmsIbfWy3dyHca68diVog8+BgSYRMPbUX8VFPGiqbC+WLMofb+JpfztQul0WLP913p27uE6Rnvwcj9xRe8Log0iRWEk885clRnerE6Czumbn2PgN/5tczOX3qG2I4uU48Zymh3ckK0pxml6Gx6mD5g4eFHubharIpD6D8D3mtZo4oiPvgB3xYZQqIZKjqbn6gkPsPQMZP1Y1+fNHALpPCAKlnSCR1wJ2ekZRatuPI0ud8+nqoIN4+HhCTQixLXdZQPPAdX5vrDyGWz8TDZTNIjas1nkg/eAhCXruQgbnP/5KpFQqmJOCY//MPhbLmWgLne8+Eu294DbPTlXyiIa70D70sjLv7M1QB0snBFUeOvZlSTqPbWOpwDxBrRLBChTG8VPYdwwZNuOAGJfpK3M+8tReRYQ5iujc5FeF/0hDDEPHPthSfrKSPmQOdw==","lnYKqHhwrA")

    
    
    