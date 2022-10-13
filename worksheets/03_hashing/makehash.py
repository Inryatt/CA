from base64 import b64decode, b64encode
import readline
from genarr import genarr
from digest import digest
import sys

def makehash_old():
    for i in range(int(sys.argv[2])):
        randb=genarr(int(sys.argv[1]))
        with open("randbytes","wb") as f:
            f.write(randb)
        with open('randbytes',"rb") as f:
            arr=f.readline()
        d=digest(arr)

        with open('digests',"a+b") as f:
            f.write(b64encode(d)+b"\n")


def makehash():
        randb=genarr(64)
        hash=digest(randb)
        return b64encode( hash)
        