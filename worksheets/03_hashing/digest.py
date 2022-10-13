
from base64 import b64decode, b64encode
import sys
from cryptography.hazmat.primitives import hashes

def digest(input:bytes)-> str:
    digest = hashes.Hash(hashes.MD5())
    digest.update(input)
    return digest.finalize()

def main():
    text =b""
    with open(sys.argv[1],"r+b") as f:
        for line in f.readlines():
            text += line
    out=digest(text)
    with open("digests", "a+b") as f:
        f.write(b64encode(out)+b'\n')
    

if __name__=="__main__":
    main()
