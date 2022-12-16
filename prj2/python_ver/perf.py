import time
from cryptography.hazmat.primitives.asymmetric.padding import PSS
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15 as PKCS1
from keygen import rsa_keygen
from sign import *
from cryptography.hazmat.primitives import serialization
from verify import *

def rsa_load_keys():
    KEYS=[]
    for key_size in [1024,2048,4096]:
        with open("keys/"+str(key_size)+"_private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
            )
        with open("keys/"+str(key_size)+"_public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
            )
        KEYS.append((public_key,private_key))
    return KEYS


def ec_load_keys():
    KEYS=[]
    CURVES=["nistp","nistb","nistk"]
    for key_size in ["small","medium","large"]:
        for cr in CURVES:
            with open("keys/"+cr+"_"+key_size+"_private_key.pem", "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                )
            with open("keys/"+cr+"_"+key_size+"_public_key.pem", "rb") as f:
                public_key = serialization.load_pem_public_key(
                    f.read(),
                )
            KEYS.append((public_key,private_key))
    return KEYS

def rsa_perf():
    KEYS=rsa_load_keys()
    PADDINGS=[PSS,PKCS1]
    print(".:----------[RSA]----------:.")

    for keypair in KEYS:
        public_key, private_key = keypair
        for paddingAlgorithm in PADDINGS:

            now_measuring="Timing RSA with key size:"+str(private_key.key_size)+"and padding: "+paddingAlgorithm.name
            message = b"this is a message"
            if paddingAlgorithm == PSS:
                start = time.time()
                signature = sign_rsa_PSS(message, private_key)
            else:
                signature = sign_rsa_PKCS1(message, private_key)
            
            rsa_verify(message, signature, public_key)
            end = time.time()
            time_taken=end-start
            print(f"{now_measuring:57} --> {time_taken:15} ")


def ec_perf():
    KEYS = ec_load_keys()
    print(".:----------[EC]----------:.")
    for keypair in KEYS:
        public_key, private_key = keypair
        now_measuring="Timing EC with curve:"+ private_key.curve.name+" and key size: "+str(private_key.key_size)
        message = b"this is a message"
        start = time.time()
        signature = sign_ec(message, private_key)
        ec_verify(message, signature, public_key)
        end = time.time()
        time_taken=end-start
        print(f"{now_measuring:<40} --> {time_taken:15} ")


if __name__ == "__main__":
    rsa_perf()
    ec_perf()