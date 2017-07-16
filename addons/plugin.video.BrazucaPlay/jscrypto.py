import hashlib
import json

import base64
import pyaes
from pkcs7 import PKCS7Encoder
import os, urllib2,urllib
import cookielib





def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    target_key_size = key_size + iv_size
    derived_bytes = ""
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)

        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)

        for i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)

        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]

        number_of_derived_words += len(block)/4

    return {
        "key": derived_bytes[0: key_size * 4],
        "iv": derived_bytes[key_size * 4:]
    }

    
def encode(plaintext,passphrase,saltsize=8):
    salt= os.urandom(saltsize)
    data = evpKDF(passphrase,salt)
    decryptor = pyaes.new(data['key'], pyaes.MODE_CBC, IV=data['iv'])
    plaintext = PKCS7Encoder().encode(plaintext)
    enctext= decryptor.encrypt(plaintext)
    return base64.b64encode("Salted__"+salt+enctext)

##''if salt is provided, it should be string
##ciphertext is base64 and passphrase is string
def decode(ciphertext,passphrase,salt=None):
    ciphertext=base64.b64decode(ciphertext)
    if not salt:
        salt=ciphertext[8:16]
        ciphertext=ciphertext[16:]
    data = evpKDF(passphrase, salt)
    decryptor = pyaes.new(data['key'], pyaes.MODE_CBC, IV=data['iv'])
    d= decryptor.decrypt(ciphertext)
    return PKCS7Encoder().decode(d)

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

def gettvnDecryptedURL(cookiejar=None,globalkey="XXX",passphrase="turbo", videoid="835", ref="http://www.moje-filmy.tk/tv/tvn", pubkeyurl='http://www.moje-filmy.tk/film/cryption/getPublicKey', handshakeurl="http://www.moje-filmy.tk/film/cryption/handshake", getvideourl="http://www.moje-filmy.tk/tv/get"):

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    if cookiejar==None:
        jw=cookielib.LWPCookieJar()
    else:
        jw=cookiejar

    pubkey=getUrl(pubkeyurl,cookieJar=jw,headers=[('Referer',ref)])
    pubkey=eval(pubkey)["publickey"]
    key=encode(globalkey, passphrase)

    
    key2 = RSA.importKey(pubkey)

    
    cipher = PKCS1_v1_5.new(key2)
    ciphertext = cipher.encrypt(key)
    getpart=base64.b64encode(ciphertext)

    post={'key':getpart}
    post = urllib.urlencode(post)
    challenge=getUrl(handshakeurl,post=post,cookieJar=jw,headers=[('Referer',ref)])

    challenge=eval(challenge)["challenge"]
    cc=encode( videoid, key)

    post={'key':cc}
    post = urllib.urlencode(post)
    url=getUrl(getvideourl,post=post,cookieJar=jw,headers=[('Referer',ref)])

    url=eval(url)["url"]
    finalurl=decode(url, key)
    print finalurl
    finalurl=eval(finalurl)["url"]
    finalurl=finalurl.replace('\\/','/')
    return finalurl


#import binascii
#import hashlib
#key, iv = EVP_BytesToKey(hashlib.md5, pp, salt, 32, 16, 1)
#print key,iv
#print 1/0
#print 'salt=%s' % binascii.b2a_hex(salt)
#print 'key=%s' % binascii.b2a_hex(key)
#print 'iv =%s' % binascii.b2a_hex(iv)

#print  decode(ct,pp,salt)
#decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
#d= decryptor.decrypt(ct)
#print d

    #print pubkey
#c=cookielib.LWPCookieJar()
#print gettvnDecryptedURL(c)


