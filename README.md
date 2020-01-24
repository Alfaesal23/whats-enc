

# Whatsapp decryption of .enc files

This is a fork of the [whatsapp-web-reveng](https://github.com/sigalor/whatsapp-web-reveng) project to
do only one thing; decrypt those .enc end-to-end encrypted media files. This is for that news story
about the Saudi's hacking Bezos, where the forensics investigators couldn't decrypt the .enc file
that contained the suspect video. They suspect it might contain a virus.

So far, I can successfully decrypt JPEGs, but I can't get streaming video to decrypt. That's because
the encryption is slightly different, so that users can skip forward in a stream without having to
download the entire video. I understand the principle, just not the exact mechanics.

## Preparation

These are the instructions for getting the environment working. I've only tried under WSL
(Windows Linux), but should work on macOS, native Windows, and native Linux as well.

- Python 2.7 with the following `pip` packages installed:
  - `websocket-client` and `git+https://github.com/dpallot/simple-websocket-server.git` for acting as WebSocket server and client.
  - `curve25519-donna` and `pycrypto` for the encryption stuff.
  - `pyqrcode` for QR code generation.
  - `protobuf` for reading and writing the binary conversation format.

Just run `pip install -r requirements.txt` for all Python dependencies.

## The code

The code I added to this forked project is the file `backend/whats-enc.py`. Just
change to that directory and run it. It will download an .enc from WhatsApp and
decrypt it using a mediakey. The URL and mediakey came from a backup of my iPhone.


## What's going on

WhatsApp uses end-to-end encryption. Thus, when your friend sends an image or video
to you on the phone, only the ends can encrypt/decrypt it.

The way this works is that your friend generates a new random `mediakey` to encrypt
the video, then does the encryption. Then, the video is uploaded to WhatsApp's servers.
WhatsApp can't decrypt the video, being in the middle and not the ends.

Your friend then sends you an encrypted message containing the URL for the video
and the `mediakey` to decrypt it. This message is also encrypted so Whatsapp can't
see it.

You then download the .enc file from the URL, then decrypt it using the `mediakey`.

If you have a forensics image of an iPhone, or even just a backup, then you can
grab the URL and `mediakey`. Remember, because of end-to-end encryption, WhatsApp
itself cannot decrypt the video, only the ends. But an image of the iPhone is
one of those ends.

I used `Reincumbate iPhone Backup Extractor` on Windows to both created a backup
of my iPhone, then extract the WhatsApp message database.

The database was in the path `/Application Groups/net.whatsapp.WhatsApp.shared/chatstorage.sqlite`.

I then opened that database in `sqlitebrowser` and went to the `ZWAMEDIAITEM` database. In that database,
the column `ZMEDIAURL` holds the URL and `ZMEDIAKEY` holds the media key.

The URL for one of the rows is the following:

	https://mmg-fna.whatsapp.net/d/f/Ap2hVbW3Da_8idKFxKUVgS7AVbDymv55tXbDVZgCAUE-.enc

The media key is in a protobuf format, a binary blob. The blob decodes as:

	0a 20
	92b9365a283534d14f658481434832ba8a77267d93b637f110df9725379f2ed0
	12 20
	f404cac1135302af0381472d9c938be0205112583356bf60dc4300346f79d7ff
	18
 	d6d3a8f105
	20 00

The first field is the media key, the second field is the hash. Base64 encoding
the media key gets:

	krk2Wig1NNFPZYSBQ0gyuop3Jn2TtjfxEN+XJTefLtA=

## Running

Just run the program:

	cd backend
	python whats-enc.py

This generates the file:

	rob.jpeg

Which if you look at the code, was downloaded from the URL and decrypted.
You can open the JPEG and have a look.
