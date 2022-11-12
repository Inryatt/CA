

import sys
from keygen import keygen
from constants import EDES_BLOCK_SIZE,ROUND_NUM,DES_BLOCK_SIZE
from utils import  read_from_stdin, unpad, get_sboxes

from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad as des_unpad

def unshuffle(inp:bytes,sbox:list) -> bytes:
    #TODO
    if len(inp)!= 4 :
        print("Mismatched block size!")
        exit(1)
    in0=inp[0]
    in1=inp[1]
    in2=inp[2]
    in3=inp[3]

    out0=(in0+in1+in2+in3) %256
    out1=(in0+in1+in2) % 256
    out2=(in0+in1) % 256
    out3=in0

    out0 = sbox[out0]
    out1 = sbox[out1]
    out2 = sbox[out2]
    out3 = sbox[out3]
    if out0=="0x0":
        out0=b'\x00'
    if out1=="0x0":
        out0='\x00'
    if out2=="0x0":
        out0='\x00'
    if out3=="0x0":
        out0='\x00'

    # TODO transform the out bytes with sboxes.
    out = out0+out1+out2+out3

    return out
    # Dark magic 

def unfeistel_round(block:bytes,sbox:list) -> bytes:
    if len(block)!= EDES_BLOCK_SIZE:
        print("Mismatched block size!")
        exit(1)
    
    right = block[:4]
    left = block[4:8]

    tmp = left

    #print(f"left: {left}\nright:{right}")
    outp = unshuffle(right,sbox)
    #outp=right
    left = right
    right = bytes([a^b for a,b in zip(outp,tmp)])
    #print(f"left: {left}\nright:{right}")

    return right+left


def decrypt(password:str,input_bytes:bytes,print_to_stdout=True) -> bytes:
    """Given a password, use EDES to decrypt data in byte format"""
    key = keygen(password,32) # Length is in bytes, 32 bytes -> 256 bits
    sboxes = get_sboxes(key,print_to_stdout)

    input_blocks = [input_bytes[n:n+EDES_BLOCK_SIZE] for n in range(0, len(input_bytes),EDES_BLOCK_SIZE) ]

    for tmp in range(ROUND_NUM):
        boxnum = ROUND_NUM-tmp -1
        for i in range(len(input_blocks)):

            input_blocks[i]=unfeistel_round(input_blocks[i],sboxes[boxnum])
    #    print([i for block in input_blocks for  i in block ])

    ptext=b""
    for block in input_blocks:
        ptext+=block

    #print(ptext)
    ptext = unpad(ptext)
    #print(ptext)
    return ptext

def des_decrypt(key: bytes, input_bytes: bytes )-> bytes:
    "Decrypt something encrypted with DES using DES."
    key = keygen(key, DES_BLOCK_SIZE)  # To pass bits to bytes
    cipher = DES.new(key, DES.MODE_ECB)
    plaintext=b""
    input_bytes = [input_bytes[n:n+DES_BLOCK_SIZE] for n in range(0, len(input_bytes),DES_BLOCK_SIZE) ]
    while True:
        if len(input_bytes)==1:
                    plaintext+=des_unpad(cipher.decrypt(input_bytes[0]),DES_BLOCK_SIZE)
                    break
        else:
                    plaintext+=cipher.decrypt(input_bytes[0])
        input_bytes=input_bytes[1:]
    return plaintext



if __name__=="__main__":
    if len(sys.argv)<1:
        print("Usage: <content_to_decrypt> | python3 decrypt.py <text_key>")
        print("To use DES, append -des to the previous command.")
        print("Hint: If you used encrypt.py to encrypt, you can do:")
        print("echo encrypted | python3 decrypt.py <key>")
        exit(1)
    print("[-] Decrypting...")
    
    key = sys.argv[1].encode("utf-8")
    input_text= read_from_stdin() # TODO add verification if theres something here
    input_bytes = bytes.fromhex(input_text)
    # input_bytes=input_text.encode('utf-8')
    if len(sys.argv)>2 and sys.argv[2]=="-des":
        decrypted = des_decrypt(key,input_bytes)
    else:
        decrypted=decrypt(key,input_bytes) # TODO implement a way to get the password
    print("[!] Decrypted!")
    print(f"[-] Output: {decrypted}")
#    print(decrypted)
