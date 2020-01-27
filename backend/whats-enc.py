from whatsapp import HKDF, AESUnpad;
import base64;
import urllib2;
from Crypto.Cipher import AES;

mediaurl = "https://mmg-fna.whatsapp.net/d/f/AsnGB7gNh6Yw52MScbJyTRMo3NCmzMpesUIYyFmEZ0lR.enc"
mediaK = "TKgNZsaEAvtTzNEgfDqd5UAdmnBNUcJtN7mxMKunAPw="
seed = "WhatsApp Video Keys"

#mediaurl = "https://mmg-fna.whatsapp.net/d/f/Ap2hVbW3Da_8idKFxKUVgS7AVbDymv55tXbDVZgCAUE-.enc"
#mediaK="krk2Wig1NNFPZYSBQ0gyuop3Jn2TtjfxEN+XJTefLtA="
#seed = "WhatsApp Image Keys"


mediaKeyExpanded=HKDF(base64.b64decode(mediaK),112,seed)
macKey=mediaKeyExpanded[48:80]
mediaData= urllib2.urlopen(mediaurl).read()

file= mediaData[:-10]
mac= mediaData[-10:]
iv=mediaKeyExpanded[:16]
cipherKey= mediaKeyExpanded[16:48]

decryptor = AES.new(cipherKey, AES.MODE_CBC, iv)
imgdata=AESUnpad(decryptor.decrypt(file))

with open('rob.jpeg', 'wb') as f:
    f.write(imgdata)
