from encrypt import encrypt
from utils import read_from_stdin,get_sboxes
from decrypt import decrypt

def main():
    # receive stdin input
    key = b"testpassword"
    input_text= read_from_stdin() # TODO add verification if theres something here
    input_bytes=input_text.encode('utf-8')
    sboxes = get_sboxes(key)
    encrypted=encrypt(key,input_bytes) # TODO implement a way to get the password
    decrypted=decrypt(key,encrypted)
main()