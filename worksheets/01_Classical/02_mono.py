import sys
from utils.prep import prepare
ASCII_OFFSET=97



def encrypt(inp,key):
    out=""
    for ch in inp:
        out+= key[ord(ch)-ASCII_OFFSET]
    return out

def decrypt(inp,key):
    out=""
    for ch in inp:
        off=key.find(ch)
        out += chr(ASCII_OFFSET+off)
    return out

def main():
    if len(sys.argv)<4 or (sys.argv[1]!="-d" and sys.argv[1]!="-e"):
        print("Usage: python3 mono.py -e/-d <key_file> <input_file> <output_file>(opt)  \nThe output will be created if it doesn't exist.\nFlags:\n -d -- decrypt\n -e -- encrypt")

    # read key
    with open(sys.argv[2],"r+") as f:
        key=f.readline()
    # read input
    with open(sys.argv[3],"r+") as f:
        inp=f.readlines()

    if sys.argv[1]=="-e": # Encrypt operation
        out = prepare(inp) 
        out = encrypt(out,key)
    elif sys.argv[1]=="-d": # Decrypt operation
        inp = prepare(inp)
        out = decrypt(inp,key)
    else:
        print("Unrecognized mode.")
        exit(1)

    if len(sys.argv)==5:
        fname=sys.argv[4]
    else:
        match sys.argv[1]:
            case "-d":
                fname="mono_decrypt_out.txt"
            case "-e":
                fname="mono_encrypt_out.txt"
    with open(fname,"w+")as f:
        f.writelines(out)
    
main()

