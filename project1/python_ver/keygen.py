import os,sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def keygen(pw:bytes,len:int) -> bytes:
    salt = b"\x00"   #os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=len, # bytes --> 16*8 
        salt=salt,
        iterations=1,
    )

    key = kdf.derive(pw)
    return key

def main():
    if len(sys.argv)<2:
        print("Usage: python3 keygen.py <password>")

    pw = bytes(sys.argv[1].strip(),'utf-8')
    for b in pw:
        print(hex(b))
    key = keygen(pw,16)

    #with open(sys.argv[2],"wb+") as f:
    #    f.write(key)

if "__main__"==__name__:
    main()