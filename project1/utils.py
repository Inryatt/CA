from pathlib import Path
import sys
from constants import EDES_BLOCK_SIZE, EDES_KEY_SIZE, ROUND_NUM, SBOX_PATH, SBOX_SIZE
from keygen import keygen
from base64 import b64encode,b64decode

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


def generate_sbox(key : bytes) -> list[bytes]:
    box=[bytes([b]) for b in range(SBOX_SIZE)]
    #TODO
    return box

def salt_key(key:bytes) -> bytes:
    salt=0
    for b in key:
        salt = salt + b
    
    keycopy = key+str(salt).encode('utf-8')

    return keygen(keycopy,32)

def transform_key(key:bytes) -> bytes:
    print(key)
    key = key + b'1'
    print(key)
    return key

def get_sboxes(key:bytes)->list[bytes]:
    sboxes=[]
    i=0

    boxpath = SBOX_PATH+ b64encode(salt_key(key)).decode('utf-8')
    boxpath=Path(boxpath)
    boxpath.parent.mkdir(exist_ok=True, parents=True)

    if boxpath.exists():
        with open(boxpath, 'r') as f:
            # Read S-boxes from file
            for line in f.readlines():
                sboxes[i]=line.split(",")
            if sboxes[i][-1] =="":
                sboxes[i][-1].pop()
            i+=1
    else:
        sboxes=[]
        for i in range(ROUND_NUM):
            key = transform_key(key)
            sboxes.append(generate_sbox(key))
        # Write S-Boxes to file
        with open(boxpath, "w+") as f:
            for sbox in sboxes:
                for b in sbox:
                    str_b=b.hex()
                    f.write(str_b+", ")
                f.write('\n')
    return sboxes

if __name__ == "__main__":
    if len(sys.argv) <2 :
        print("Only run this directly to generate sboxes! (for testing purposes)\nUsage: python3 utils.py <text_key>")
        exit(1)
    key = sys.argv[1]
    key = keygen(key.encode('utf-8'),EDES_KEY_SIZE) # Length is in bytes, 32 bytes -> 256 bits

    get_sboxes(key)    