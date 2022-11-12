from os import urandom
import encrypt,decrypt,utils
from time import clock_gettime,CLOCK_REALTIME
import sys
def main(): 
    buffer = urandom(4096) # 4kib
    # EDES
    edes_times=[]
    des_times=[]
    if "edes" in sys.argv:
     for i in range(100):
        key=urandom(10) # can be any size :)
        start = clock_gettime(CLOCK_REALTIME)
        encrypted=encrypt.encrypt(key,buffer,False)
        decrypted=decrypt.decrypt(key,encrypted,False)
        end = clock_gettime(CLOCK_REALTIME)

        if decrypted!=buffer:
            print("[!] Something failed here!")
            exit(1)
        edes_times.append(end-start)
     print(min(edes_times))

    if "des" in sys.argv:
     for i in range(1000):
        key=urandom(10) # can be any size :)
        start = clock_gettime(CLOCK_REALTIME)
        encrypted=encrypt.des_encrypt(key,buffer)
        decrypted=decrypt.des_decrypt(key,encrypted)
        end = clock_gettime(CLOCK_REALTIME)

        if decrypted!=buffer:
            print("[!] Something failed here!")
            exit(1)
        des_times.append(end-start)
     print(min(des_times))


if __name__=="__main__":
    main()