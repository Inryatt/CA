import json
from encryptfile import encrypt
import sys



def main():
    if len(sys.argv)<4:
        print("Usage: python3 encrypt_image.py AES <mode> <key file> <image file>")

    key=b""
    with open(sys.argv[3],"rb") as f:
        for line in f.readlines():
            key+=line

    algo=sys.argv[1]
    mode=sys.argv[2]

    infile = sys.argv[4]
    outfile = infile.split(".")[0]+"-"+mode+".bmp"
    with open(infile,"rb") as f:
        f.seek(0)
        header = f.read(54)
    
 
    cipherdata=encrypt(key,infile,outfile,algo,mode)
    with open('def_img.txr' ,"w+") as f:
        #f.write(str(cipherdata))
         f.write(json.dumps(cipherdata)) #-- issues with bytes due to IV

    #with open(outfile,"wb") as f:
    #    f.seek(0)
    #    f.write(header)
    # dd if=security.bmp of=security-ECB.bmp bs=1 count=54 conv=notrunc
if "__main__"==__name__:
    main()