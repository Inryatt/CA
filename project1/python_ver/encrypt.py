import sys

from keygen import keygen
from constants import EDES_BLOCK_SIZE, ROUND_NUM, EDES_KEY_SIZE,DES_BLOCK_SIZE 
from utils import get_sboxes, pad, read_from_stdin
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad as des_pad


def shuffle(inp: bytes, sbox: list) -> bytes:
    if len(inp) != 4:
        print("Mismatched block size!")
        exit(1)
    in0 = inp[0]
    in1 = inp[1]
    in2 = inp[2]
    in3 = inp[3]
    out0 = (in0+in1+in2+in3) % 256
    out1 = (in0+in1+in2) % 256
    out2 = (in0+in1) % 256
    out3 = in0

    out0 = sbox[out0]
    out1 = sbox[out1]
    out2 = sbox[out2]
    out3 = sbox[out3]
    
    out = out0+out1+out2+out3
    return out


def feistel_round(block: bytes, sbox: list) -> bytes:
    if len(block) != EDES_BLOCK_SIZE:
        print("Mismatched block size!")
        exit(1)
    left = block[:4]
    tmp = left
    right = block[4:8]

    outp = shuffle(right, sbox)
    left = right
    right = bytes([a ^ b for a, b in zip(outp, tmp)])

    return left+right


def encrypt(password: bytes, input_bytes: bytes,print_to_stdout=True) -> bytes:
    """Given a password, use EDES to encrypt data in byte format"""
    # Length is in bytes, 32 bytes -> 256 bits
    key = keygen(password, EDES_KEY_SIZE)
    sboxes = get_sboxes(key,print_to_stdout)
    input_blocks = [input_bytes[n:n+EDES_BLOCK_SIZE]
                    for n in range(0, len(input_bytes), EDES_BLOCK_SIZE)]

    # pad the input blocks (only last block is affected) (or a new block is added!)
    input_blocks = pad(input_blocks)

    ciphertext = b""
    for tmp in range(ROUND_NUM):
        for i in range(len(input_blocks)):
            input_blocks[i] = feistel_round(input_blocks[i], sboxes[tmp])

    for block in input_blocks:
        ciphertext += block
    return ciphertext


def des_encrypt(key: bytes, input_bytes: bytes) -> bytes:
    key = keygen(key, DES_BLOCK_SIZE)
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext=b""
    input_bytes = [input_bytes[n:n+DES_BLOCK_SIZE] for n in range(0, len(input_bytes),DES_BLOCK_SIZE) ]

    while True:
        if len(input_bytes)==1:
            ciphertext+=cipher.encrypt(des_pad(input_bytes[0],DES_BLOCK_SIZE))
            break
        else:
            ciphertext+=cipher.encrypt(input_bytes[0])
        input_bytes=input_bytes[1:]
    return ciphertext

    

if __name__ == "__main__":
    if len(sys.argv) < 1 or len(sys.argv)>3:
        print("Usage: <content_to_encrypt> | python3 encrypt.py <text_key>")
        print("If you wish to encrypt with DES, append -des to the previous command.")
        exit(1)
    print("[-] Encrypting..")
    key = sys.argv[1].encode("utf-8")
    input_text = read_from_stdin()  
    input_bytes = input_text.encode('utf-8')
    print([i for i in input_bytes])
    
    if len(sys.argv) > 2 and sys.argv[2] == "-des":
        encrypted = des_encrypt(key, input_bytes)
    else:
        encrypted = encrypt(key, input_bytes)
    print("[-] Encrypted!")
    print("[-] Output stored in file 'encrypted'")
    print(encrypted.hex())
    with open("encrypted", "w+") as f:
        f.write(encrypted.hex())


