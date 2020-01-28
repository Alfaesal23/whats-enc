from whatsapp import HKDF, AESUnpad;
import base64;
import urllib2;
from Crypto.Cipher import AES;

#Example of MP4 video
mediaurl = "https://mmg-fna.whatsapp.net/d/f/AsnGB7gNh6Yw52MScbJyTRMo3NCmzMpesUIYyFmEZ0lR.enc"
mediakey = "TKgNZsaEAvtTzNEgfDqd5UAdmnBNUcJtN7mxMKunAPw="
salt = "WhatsApp Video Keys"

#Example grabbing JPEG instead of MP4
#mediaurl = "https://mmg-fna.whatsapp.net/d/f/Ap2hVbW3Da_8idKFxKUVgS7AVbDymv55tXbDVZgCAUE-.enc"
#mediakey="krk2Wig1NNFPZYSBQ0gyuop3Jn2TtjfxEN+XJTefLtA="
#salt = "WhatsApp Image Keys"


mediaKeyExpanded = HKDF(base64.b64decode(mediakey),112,salt)
iv = mediaKeyExpanded[:16]
cipherKey = mediaKeyExpanded[16:48]
macKey = mediaKeyExpanded[48:80]

mediaData = urllib2.urlopen(mediaurl).read()
file = mediaData[:-10]
mac = mediaData[-10:]


decryptor = AES.new(cipherKey, AES.MODE_CBC, iv)
imgdata=AESUnpad(decryptor.decrypt(file))

with open('rob.mp4', 'wb') as f:
    f.write(imgdata)

print("file written to rob.mp4")
