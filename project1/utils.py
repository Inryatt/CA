from hashlib import shake_256
from pathlib import Path
from random import sample
import sys
from weakref import finalize
from constants import EDES_BLOCK_SIZE, EDES_KEY_SIZE, ROUND_NUM, SBOX_PATH, SBOX_SIZE
from keygen import keygen
from base64 import b64encode,b64decode
from cryptography. hazmat.primitives import hashes

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
    #print(to_remove)
    input_text=input_text[:-to_remove]
    return input_text

def read_from_stdin() -> str:
    out=""
    for line in sys.stdin:
        out=out+line.strip()
    return out


def generate_sbox(key : bytes) -> list[bytes]:
    # Derive key to get our seed
    digest = hashes.Hash(hashes.SHAKE256(256))
    digest.update(key)
    seed = digest.finalize()
    seedbox=[]
    #print(seed)
    for ch in seed:
        seedbox.append(ch)
 
    box = [str(i).encode('utf-8') for i in range(256)]
    samplebox = [str(i).encode('utf-8') for i in range(256)]

    # the values in seedbox the shift in position that will apply to each
    # element of the s-box

    seedbox=[(seedbox[i]+i)%len(seedbox) for i in range(len(seedbox))]
    
    # Shuffle the box contents ( seedbox -> shift values; samplebox-> copy of box)
    for i in range(len(seedbox)):
        samplebox=box
        tmp=box[box.index(samplebox[i])]
        box.remove(samplebox[i])
        box.insert(seedbox[i],tmp)

    #TODO
    # print(sorted([int(x.decode('utf-8')) for x in box])) --> To verify that the box contains all the elements, as it should
    #for i in range(256):
    #    if int(box[i].decode('utf-8'))==i:
    #        print("BAD")
    #exit(1)
    #print(box)
    return box

def salt_key(key:bytes) -> bytes:
    salt=0
    for b in key:
        salt = salt + b
    
    keycopy = key+str(salt).encode('utf-8')

    return keygen(keycopy,32)

def transform_key(key:bytes) -> bytes:
    key = key + b'1'
    return key
    # NEEDS REDO-ING!!!!!


def get_sboxes(key:bytes)->list[bytes]:
    sboxes=[]
    i=0

    filename_box= bytes.hex(salt_key(key))#.decode('ascii')
    boxpath = SBOX_PATH+filename_box
    boxpath=Path(boxpath)
    boxpath.parent.mkdir(exist_ok=True, parents=True)

    if boxpath.exists():
        with open(boxpath, 'r') as f:
            # Read S-boxes from file
            for line in f.readlines():
                line = line.strip()
                print(line)
                sboxes.append(line.split(", "))
                #print(sboxes)
            for i in range(len(sboxes)):
                if sboxes[i][-1]=='':
                    sboxes[i].pop(-1)
                for j in range(len(sboxes[i])):
                    #to_read=sboxes[i][j].strip('0x')
                    to_read =sboxes[i][j][2:]
                    #if to_read=="":
                    #    continue
                    print(to_read)
                    ##print(f"A{to_read}A")
                    #if len(to_read)<2:
                    #    to_read='0'+to_read
                    ##print(to_read)
                    sboxes[i][j] = bytes.fromhex(to_read)
                print("\n=====================================\n")
    else:
        sboxes=[]
        for i in range(ROUND_NUM):
            key = transform_key(key)
            sboxes.append(generate_sbox(key))
        print(sboxes)
        # Write S-Boxes to file
        with open(boxpath, "w+") as f:
            for sbox in sboxes:
                i=0
                for b in sbox:
                    # print(int(b))
                    str_b=hex(int(b))
                    # print(str_b)
                    f.write(str_b)
                    i+=1
                    if i!=256:
                        f.write(', ')

                f.write('\n')
    #print(sboxes)
    return sboxes

if __name__ == "__main__":
    if len(sys.argv) <2 :
        print("Only run this directly to generate sboxes! (for testing purposes)\nUsage: python3 utils.py <text_key>")
        exit(1)
    key = sys.argv[1]
    key = keygen(key.encode('utf-8'),EDES_KEY_SIZE) # Length is in bytes, 32 bytes -> 256 bits

    get_sboxes(key)