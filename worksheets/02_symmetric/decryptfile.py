import json
import os
import sys


from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from keygen import keygen
from base64 import b64decode
DES_BLOCK_SIZE = 8


def decrypt(key, infile, outfile, algo, mode, iv):
    with open(outfile, "wb") as f: # clean output file
        f.write(b"")
    infile = open(infile, "r+b")
    outfile = open(outfile, "w+b")

    match algo:
        case "AES":
            good = True
            algo = algorithms.AES(key)
        case "DES":
            key = keygen(key, DES_BLOCK_SIZE)  # To pass bits to bytes
            good = False
            cipher = DES.new(key, DES.MODE_ECB)
        case _:
            print("Invalid algorithm!")
            exit(1)
    if good:
        match mode.upper():
            case "CBC":
                mode = modes.CBC(iv)
            case "ECB":
                mode = modes.ECB()
            case "OFB":
                mode = modes.OFB(iv)
            case "CFB":
                mode = modes.CFB(iv)
            case "CTR":
                mode = modes.CTR(iv)
            case _:
                print("Invalid mode!")
                exit(1)
        cipher = Cipher(algo, mode)
    else:
        while True:
            txt = infile.read(DES_BLOCK_SIZE)

            if not txt:
                break
            else:
                if len(txt) < 8:
                    pt = cipher.decrypt(txt)
                    # print(pt)
                    outfile.write(unpad(pt, DES_BLOCK_SIZE))
                    break
                else:
                    pt = cipher.decrypt(txt)
                    # print(pt)
                    outfile.write(pt)
        return

    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algo.block_size).unpadder()

    while True:
        txt = infile.read(algo.block_size)

        if len(txt)<algo.block_size:
            txt = decryptor.update(txt)
            pt = unpadder.update(txt) + unpadder.finalize()
            outfile.write(pt)
            break
        else:
            pt = decryptor.update(txt)
            outfile.write(pt)
    outfile.close()
    infile.close()


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python3 decryptfile.py <description file> <key file> <input file> <output file>")

    key = b""
    with open(sys.argv[2], "rb") as f:
        for line in f.readlines():
            key += line
    with open(sys.argv[1], 'r+') as f:
        cipherdata = f.readline()
    cipherdata = json.loads(cipherdata)
    infile = sys.argv[3]
    outfile = sys.argv[4]

    # print((b64decode(cipherdata['iv'])))
    decrypt(key, infile, outfile,
            cipherdata['algo'], cipherdata['mode'], b64decode(cipherdata['iv']))


if "__main__"==__name__:
    main()