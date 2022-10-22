import sys
from constants import EDES_BLOCK_SIZE

def pad(input_blocks:list) -> list:
    """Pads a list of blocks with plaintext for EDES"""
    
    input= input_blocks[-1]
    missing = EDES_BLOCK_SIZE - len(input)
    if missing == 0:
        padding=b""
        for i in range(EDES_BLOCK_SIZE):
            padding+=str(EDES_BLOCK_SIZE).encode('utf-8')
        input_blocks+=[padding]
    else:
        for i in range(missing):
            input+=str(missing).encode('utf-8')
        input_blocks[-1] = input
    return input_blocks

def unpad(input_text:str) -> str:
    """Unpads a string previously padded. Might work with bytes, idk"""
    to_remove=int(input_text[-1])
    print(to_remove)
    input_text=input_text[:-to_remove]
    return input_text

def read_from_stdin() -> str:
    out=""
    for line in sys.stdin:
        out=out+line.strip()
    return out
