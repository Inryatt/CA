import os
import sys


def genarr(lenb:int):
    """Returns random bytes of the specified length"""
    return os.urandom(lenb)

def main():
    outf="randbytes"
    if len(sys.argv)<2:
        print("Usage: python3 genarr.py <size> <optional: outputfile>")
        exit(1)
    else:
        try:
            lenb = int(sys.argv[1])
        except:
            print("First argument must be numeric. And preferrably not 0 or too high. But that's on you.")
            exit(1)
        if len(sys.argv)>2:
            outf=sys.argv[2]
    with open(outf,"w+b") as f:
        f.write(genarr(lenb))
    
if __name__=="__main__":
    main()