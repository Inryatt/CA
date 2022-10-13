import os, sys, json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from Crypto.Cipher import DES
from keygen import keygen
from Crypto.Util.Padding import pad
from base64 import b64encode

DES_BLOCK_SIZE = 8


def encrypt(key, infile,outfile,algo, mode:str) -> dict:
    cipherdata = {
        "algo":algo,
        "mode":mode,
        "iv":""
            }

    with open(outfile,"wb") as f:
        f.write(b"")
    f = open(outfile,"w+b")
    ptext = open(infile,"r+b")
    match algo:
        case "AES":
            algo = algorithms.AES(key)
            good=True
        case "DES":
            key = keygen(key,DES_BLOCK_SIZE)
            cipher = DES.new(key, DES.MODE_ECB)
            good = False
        case _ :
            print("Invalid algorithm!")
            exit(1)
  
    if good:
        # It's not DES.

        ivsize=int(algo.block_size/8)
        iv = os.urandom(algo.block_size)[:ivsize]
        cipherdata['iv']=b64encode(iv).decode('utf-8')
        match mode.upper():
            case "CBC":
                mode = modes.CBC(iv)
            case "ECB":
                mode = modes.ECB()
                cipherdata['iv']=""
            case "OFB":
                mode = modes.OFB(iv)
            case "CFB":
                mode = modes.CFB(iv)
            case "CTR":
                mode = modes.CTR(iv)
            case _ :
                print("Invalid mode!")
                exit(1)
        cipher = Cipher(algo, mode)
       
    else:
        # It's DES. 
        while True:
            txt=ptext.read(8)
            print(txt)
            if not txt:
                #f.write(cipher.encrypt(pad(b"",DES_BLOCK_SIZE)))
                break
            else:
               # ct = encryptor.update(padder.update(txt))
                if len(txt)<8:
                    f.write(cipher.encrypt(pad(txt,DES_BLOCK_SIZE)))
                    break
                else:
                    f.write(cipher.encrypt(txt))
        return  cipherdata


    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algo.block_size).padder()

    while True:
        txt=ptext.read(algo.block_size)
        if len(txt)<algo.block_size:
            txt=padder.update(txt)+padder.finalize()
            ct = encryptor.update(txt)+encryptor.finalize() 
            f.write(ct)
            break
        else:
            ct = encryptor.update(txt)
            f.write(ct)
    f.close()
    ptext.close()
    return cipherdata


def main():
    if len(sys.argv)<4:
        print("Usage: python3 keygen.py <DES/AES> <mode> <key file> <plaintext file> <ciphertext file> <definition file>")

    key=b""
    with open(sys.argv[3],"rb") as f:
        for line in f.readlines():
            key+=line

    algo=sys.argv[1]
    mode=sys.argv[2]

    infile = sys.argv[4]
    outfile = sys.argv[5]
    definition = sys.argv[6]

 
    cipherdata=encrypt(key,infile,outfile,algo,mode)
    
    with open(definition ,"w+") as f:
        #f.write(str(cipherdata))
         f.write(json.dumps(cipherdata)) #-- issues with bytes due to IV

if "__main__"==__name__:
    main()