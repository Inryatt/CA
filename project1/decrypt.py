
from keygen import keygen
from constants import EDES_BLOCK_SIZE,ROUND_NUM
from utils import  unpad


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
    #out0=in0
    #out1=in1
    #out2=in2
    #out3=in3

    # TODO transform the out bytes with sboxes.



    return bytes([out0,out1,out2,out3])
    # Dark magic 

def unfeistel_round(block:bytes,sbox:list) -> bytes:
    if len(block)!= EDES_BLOCK_SIZE:
        print("Mismatched block size!")
        exit(1)
    
    right = block[:4]
    left = block[4:8]
    tmp = left

    print(f"left: {left}\nright:{right}")
    outp = unshuffle(right,sbox)
    #outp=right
    left = right
    right = bytes([a^b for a,b in zip(outp,tmp)])
    print(f"left: {left}\nright:{right}")

    return right+left


def decrypt(password:str,input_bytes:bytes) -> bytes:
    print("Decrypting...")

    """Given a password, use EDES to decrypt data in byte format"""
    key = keygen(password,32) # Length is in bytes, 32 bytes -> 256 bits
    input_blocks = [input_bytes[n:n+EDES_BLOCK_SIZE] for n in range(0, len(input_bytes),EDES_BLOCK_SIZE) ]
    print("original:")
    for block in input_blocks:
        for ch in block:
            print(hex(ch),end=" ")
    print()
    print()
    for tmp in range(ROUND_NUM):
        for i in range(len(input_blocks)):
            input_blocks[i]=unfeistel_round(input_blocks[i],[''])
        
        # print(input_blocks)
        for block in input_blocks:
            for ch in block:
             print(hex(ch),end=" ")
            print()

    ptext=b""
    for block in input_blocks:
        ptext+=block

    ptext=ptext.decode('utf-8')
    #unpad text    
    print(ptext)

    ptext = unpad(ptext)
    print(ptext)
    return ptext

if __name__=="__main__":
    print("dont run this directly.")