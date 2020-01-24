from whatsapp import HKDF, AESUnpad;
import base64;
import urllib2;
from Crypto.Cipher import AES;

mediaK="krk2Wig1NNFPZYSBQ0gyuop3Jn2TtjfxEN+XJTefLtA="

mediaKeyExpanded=HKDF(base64.b64decode(mediaK),112,"WhatsApp Image Keys")
macKey=mediaKeyExpanded[48:80]
mediaData= urllib2.urlopen("https://mmg-fna.whatsapp.net/d/f/Ap2hVbW3Da_8idKFxKUVgS7AVbDymv55tXbDVZgCAUE-.enc").read()

file= mediaData[:-10]
mac= mediaData[-10:]
iv=mediaKeyExpanded[:16]
cipherKey= mediaKeyExpanded[16:48]

decryptor = AES.new(cipherKey, AES.MODE_CBC, iv)
imgdata=AESUnpad(decryptor.decrypt(file))

with open('rob.jpeg', 'wb') as f:
    f.write(imgdata)
