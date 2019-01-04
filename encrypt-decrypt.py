import os
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def usage():
	print("""
    usage: script.py [option] <key> <file> 

    example: chaos.py --encrypt 'letmein' 'bank.txt'
             chaos.py --decrypt 'password' 'accounts.txt'
    """)

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "en" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(getKey(key), AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = "de" + filename

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(getKey(key), AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)

def getKey(password):
            hasher = SHA256.new(password.encode('utf-8'))
            return hasher.digest()

def main():
	if len(sys.argv) <= 3:
		print(usage())
		exit(1)
	if sys.argv[1] == '-e' or sys.argv[1] == '--encrypt':
		encrypt(sys.argv[2], sys.argv[3])
		exit(0)
	elif sys.argv[1] == '-d' or sys.argv[1] == '--decrypt':
		decrypt(sys.argv[2], sys.argv[3])
		exit(0)
	else:
		print(usage())
		exit(1)

if __name__ == '__main__':
	main()
