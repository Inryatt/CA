import sys

from os import read
from keygen import keygen
from constants import EDES_BLOCK_SIZE, ROUND_NUM, EDES_KEY_SIZE,DES_BLOCK_SIZE 
from utils import get_sboxes, pad, read_from_stdin
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad as des_pad


def shuffle(inp: bytes, sbox: list) -> bytes:
    # TODO
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

    # This is needed for an edge case :c
    if out0 == "0x0":
        out0 = b'\x00'
    if out1 == "0x0":
        out0 = '\x00'
    if out2 == "0x0":
        out0 = '\x00'
    if out3 == "0x0":
        out0 = '\x00'

    out = out0+out1+out2+out3
    return out
    # Dark magic


def feistel_round(block: bytes, sbox: list) -> bytes:
    #print("using box :")
    # print(sbox)
    if len(block) != EDES_BLOCK_SIZE:
        print("Mismatched block size!")
        exit(1)
    # print(sbox)
    # print()
    left = block[:4]
    tmp = left
    right = block[4:8]
    #print(f"left: {left}\nright:{right}")

    outp = shuffle(right, sbox)
    # outp=right
    left = right
    right = bytes([a ^ b for a, b in zip(outp, tmp)])
    #print(f"left: {left}\nright:{right}")

    return left+right


def encrypt(password: bytes, input_bytes: bytes) -> bytes:
    """Given a password, use EDES to encrypt data in byte format"""
    print("Encrypting...")
    # Length is in bytes, 32 bytes -> 256 bits
    key = keygen(password, EDES_KEY_SIZE)
    sboxes = get_sboxes(key)
    input_blocks = [input_bytes[n:n+EDES_BLOCK_SIZE]
                    for n in range(0, len(input_bytes), EDES_BLOCK_SIZE)]

    # pad block
    input_blocks = pad(input_blocks)

    # print("original:")
    # for block in input_blocks:
    #    for ch in block:
    #        print(hex(ch),end=" ")
    # print()
    # print()

    ciphertext = b""
    for tmp in range(ROUND_NUM):
        for i in range(len(input_blocks)):
            input_blocks[i] = feistel_round(input_blocks[i], sboxes[tmp])

        # print(input_blocks)
        # for block in input_blocks:
        #     for ch in block:
        #      print(hex(ch),end=" ")
        #     print()
        # print("end round")

    for block in input_blocks:
        ciphertext += block
    return ciphertext


def des_encrypt(key: bytes, input_bytes: bytes) -> bytes:
    # TODO this function stub
    key = keygen(key, DES_BLOCK_SIZE)
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext=b""
    while True:
            txt=input_bytes[:DES_BLOCK_SIZE]
            print(txt)
            if not txt:
                #f.write(cipher.encrypt(pad(b"",DES_BLOCK_SIZE)))
                break
            else:
               # ct = encryptor.update(padder.update(txt))
                if len(txt)<DES_BLOCK_SIZE:
                    ciphertext+=cipher.encrypt(des_pad(txt,DES_BLOCK_SIZE))
                    break
                else:
                    ciphertext+=cipher.encrypt(txt)
            input_bytes=input_bytes[DES_BLOCK_SIZE:]
    return ciphertext

    


if __name__ == "__main__":
    if len(sys.argv) < 1 or len(sys.argv)>3:
        print("Usage: <content_to_encrypt> | python3 encrypt.py <text_key>")
        print("If you wish to encrypt with DES, append -des to the previous command.")
        exit(1)
    print("[-] Encrypting..")
    key = sys.argv[1].encode("utf-8")
    input_text = read_from_stdin()  # TODO add verification if theres something here
    input_bytes = input_text.encode('utf-8')
    if len(sys.argv) > 2 and sys.argv[2] == "-des":
        encrypted = des_encrypt(key, input_bytes)
    else:
        encrypted = encrypt(key, input_bytes)
    print("[-] Encrypted!")
    print("[-] Output stored in file 'encrypted'")
    print(encrypted)
    print(encrypted.hex())
    with open("encrypted", "w+") as f:
        f.write(encrypted.hex())
