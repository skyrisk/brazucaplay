import base64,binascii

def RijndaelManaged_encrypt(plan_text , key, iv ='\0'*16):

    if len(key)<32:
        key=key+chr(0)*(32-len(key))

    from pkcs7 import PKCS7Encoder
    encoder = PKCS7Encoder()
    plan_text=encoder.encode(plan_text)

    import pyaes
    decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
    ds1 = decryptor.encrypt(plan_text)

    return base64.b64encode(ds1)
    
#print RijndaelManaged_encrypt('I6Vlebp6syWB5U+gEdeKQmYm','64328547SimpsonsTV')
