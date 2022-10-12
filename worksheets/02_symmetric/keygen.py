import os,sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def keygen(pw,len):

    salt = b'x/00'#os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=len, # bytes --> 16*8 
        salt=salt,
        iterations=2000,
    )

    key = kdf.derive(pw)
    return key

def main():
    if len(sys.argv)<3:
        print("Usage: python3 keygen.py <password> <output file name>")

    pw = bytes(sys.argv[1].strip(),'utf-8')
    key = keygen(pw,16)

    with open(sys.argv[2],"wb+") as f:
        f.write(key)

if "__main__"==__name__:
    main()