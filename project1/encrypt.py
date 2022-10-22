from os import read
import sys
from keygen import keygen

from constants import EDES_BLOCK_SIZE,ROUND_NUM
from utils import pad,read_from_stdin

def shuffle(inp:bytes,sbox:list) -> bytes:
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
    #out0=in0
    #out1=in1
    #out2=in2
    #out3=in3
    # TODO transform the out bytes with sboxes.



    return bytes([out0,out1,out2,out3])
    # Dark magic



def feistel_round(block:bytes,sbox:list) -> bytes:
    if len(block)!= EDES_BLOCK_SIZE:
        print("Mismatched block size!")
        exit(1)
    
    left = block[:4]
    tmp = left
    right = block[4:8]
    print(f"left: {left}\nright:{right}")
    outp = shuffle(right,sbox)
    #outp=right
    left = right
    right = bytes([a^b for a,b in zip(outp,tmp)])
    print(f"left: {left}\nright:{right}")

    return left+right



def encrypt(password:str,input_bytes:bytes) -> bytes:
    """Given a password, use EDES to encrypt data in byte format"""
    print("Encrypting...")
    key = keygen(password,32) # Length is in bytes, 32 bytes -> 256 bits
    input_blocks = [input_bytes[n:n+EDES_BLOCK_SIZE] for n in range(0, len(input_bytes),EDES_BLOCK_SIZE) ]
    
    # pad block
    input_blocks = pad(input_blocks)

    print("original:")
    for block in input_blocks:
        for ch in block:
            print(hex(ch),end=" ")
    print()
    print()

    ciphertext=b""
    for tmp in range(ROUND_NUM):
        for i in range(len(input_blocks)):
            input_blocks[i]=feistel_round(input_blocks[i],[''])
        #
        # print(input_blocks)
        for block in input_blocks:
            for ch in block:
             print(hex(ch),end=" ")
            print()
        print("end round")

    for block in input_blocks:
        ciphertext+=block
    return ciphertext
        

def des_encrypt(password:str,input_bytes:bytes)-> bytes:
    # TODO this function stub
    pass


if __name__=="__main__":
    print("dont run this directly.")