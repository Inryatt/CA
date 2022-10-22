from encrypt import encrypt
from utils import read_from_stdin
from decrypt import decrypt

def main():
    # receive stdin input
    input_text= read_from_stdin() # TODO add verification if theres something here
    input_bytes=input_text.encode('utf-8')
    encrypted=encrypt(b"testpassword",input_bytes) # TODO implement a way to get the password
    decrypted=decrypt(b"testpassword",encrypted)
main()