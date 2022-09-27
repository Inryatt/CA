from re import ASCII
import sys
from utils.prep import prepare
ASCII_OFFSET=97


# math sourced from https://github.com/odysseus/vigenere
def encrypt(inp,key):
    out=""
    key = [ord(i) for i in key]
    inp = [ord(i) for i in inp]
    for i in range(len(key)):
        out += chr(((inp[i]-ASCII_OFFSET)+(key[i]-ASCII_OFFSET))%26 + ASCII_OFFSET)
    return out

def decrypt(inp,key):
    out=""
    key = [ord(i) for i in key]
    inp = [ord(i) for i in inp]
    for i in range(len(key)):
        out += chr((inp[i] -key[i] + 26) % 26 + ASCII_OFFSET)


    return out

def fit_key(key,length):
    outkey=""
    while len(outkey)<length:
        outkey+=key
    key =outkey[:length]
    return key

def main():

    if len(sys.argv)<4 or (sys.argv[1]!="-d" and sys.argv[1]!="-e"):
        print("Usage: python3 03_poly.py -e/-d <key_file> <input_file> <output_file>(opt)  \nThe output will be created if it doesn't exist.\nFlags:\n -d -- decrypt\n -e -- encrypt")

    # Fetch Key
    with open(sys.argv[2],"r+") as f:
        key=f.readline()
    
    with open(sys.argv[3],"r+") as f:
        inp=f.readlines()
    out = prepare(inp) 
    key=fit_key(key,len(out))    
    if sys.argv[1]=="-e": # Encrypt operation
        out = encrypt(out,key)
    elif sys.argv[1]=="-d": # Decrypt operation
        out = decrypt(out,key)
    else:
        print("Unrecognized mode.")
        exit(1)
    if len(sys.argv)==5:
        fname=sys.argv[4]
    else:
        match sys.argv[1]:
            case "-d":
                fname="poly_decrypt_out.txt"
            case "-e":
                fname="poly_encrypt_out.txt"
    with open(fname,"w+")as f:
        f.writelines(out)

if __name__=="__main__":
    main()

