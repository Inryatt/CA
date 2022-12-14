from cryptography.hazmat.primitives.asymmetric.padding import PSS
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15 as PKCS1
from keygen import rsa_keygen
from sign import *
from cryptography.hazmat.primitives import serialization


def load_keys():
    KEYS=[]
    for key_size in [1024,2048,4096]:
        with open(str(key_size)+"_private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
            )
        with open(str(key_size)+"_public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
            )
        KEYS.append((public_key,private_key))
    return KEYS

def rsa_perf():
    KEYS=load_keys()
    PADDINGS=[PSS,PKCS1]
    for keypair in KEYS:
        public_key, private_key = keypair
        for paddingAlgorithm in PADDINGS:
            
            message = b"this is a message"
            if paddingAlgorithm == PSS:
                signature = sign_rsa_PSS(message, private_key)
            else:
                signature = sign_rsa_PKCS1(message, private_key)


if __name__ == "__main__":
    rsa_perf()