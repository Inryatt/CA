import time
from cryptography.hazmat.primitives.asymmetric.padding import PSS
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15 as PKCS1
from keygen import rsa_keygen
from sign import *
from cryptography.hazmat.primitives import serialization
from verify import *


n_size = 1000
m_size = 100


def rsa_load_keys():
    KEYS = []
    for key_size in [1024, 2048, 4096]:
        with open("../keys/"+str(key_size)+"_private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
            )
        with open("../keys/"+str(key_size)+"_public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
            )
        KEYS.append((public_key, private_key))
    return KEYS


def ec_load_keys():
    KEYS = []
    CURVES = ["nistp", "nistb", "nistk"]
    for key_size in ["small", "medium", "large"]:
        for cr in CURVES:
            with open("../keys/"+cr+"_"+key_size+"_private_key.pem", "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                )
            with open("../keys/"+cr+"_"+key_size+"_public_key.pem", "rb") as f:
                public_key = serialization.load_pem_public_key(
                    f.read(),
                )
            KEYS.append((public_key, private_key))
    return KEYS


def rsa_perf():
    KEYS = rsa_load_keys()
    PADDINGS = [PSS, PKCS1]
    print(".:----------[RSA]----------:.")
    speeds = {}
    for keypair in KEYS:
        public_key, private_key = keypair
        for paddingAlgorithm in PADDINGS:
            for n in range(n_size):

                now_measuring_short = str(
                    private_key.key_size)+"_"+paddingAlgorithm.name

                now_measuring_long = "Timed RSA with key size:" + \
                    str(private_key.key_size)+"and padding: "+paddingAlgorithm.name
                if now_measuring_short not in speeds:
                    speeds[now_measuring_short] = []
                
                message = b"this is a message"
                m_sum = 0
                start = time.time()

                for m in range(m_size):
                    if paddingAlgorithm == PSS:
                        signature = sign_rsa_PSS(message, private_key)
                    else:
                        signature = sign_rsa_PKCS1(message, private_key)

                    rsa_verify(message, signature, public_key)
                end = time.time()
                time_taken = end-start
                speeds[now_measuring_short].append(time_taken)
            smallest = min(speeds[now_measuring_short])
            speeds[now_measuring_short]= smallest/m_size
            print(f"{now_measuring_long:<40} --> {smallest/m_size:15} ")



def ec_perf():
    KEYS = ec_load_keys()
    print(".:----------[EC]----------:.")
    for keypair in KEYS:
        speeds=[]
        public_key, private_key = keypair
        now_measuring = "Timing EC with curve:" + private_key.curve.name + \
                " and key size: "+str(private_key.key_size)
        now_measuring_short = private_key.curve.name+"_"+str(private_key.key_size)
        message = b"this is a message"
        for n in range(n_size):
            
            start = time.time()
            for m in range(m_size):
                signature = sign_ec(message, private_key)
                ec_verify(message, signature, public_key)
            end = time.time()
            time_taken = end-start
            speeds.append(time_taken)
            
        print(f"{now_measuring:<40} --> {min(speeds)/m_size:15} ")


if __name__ == "__main__":
    #rsa_perf()
    ec_perf()
