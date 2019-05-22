# secret

You will need pycrypto for this script to work, the way way to get that is via pip.

pip install pycrypto
pip3 install pycrypto

usage: script.py [option] <key> <file> 

example: secret.py --encrypt 'letmein' 'bank.txt'
         secret.py --decrypt 'password' 'accounts.txt'
