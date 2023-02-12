
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def rsa_keygen(size_key:int):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size_key,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def ec_keygen(curv:str,curv_size:str):
    match curv:
        case "nistp":
            match curv_size:
                case "small":
                    curve = ec.SECP256R1() # NIST P-256
                case "medium":
                    curve = ec.SECP384R1() # NIST P-384
                case "large":
                    curve = ec.SECP521R1() # NIST P-521
        case "nistb":
            match curv_size:
                case "small":
                    curve = ec.SECT163K1() # NIST K-163
                case "medium":
                    curve = ec.SECT283K1() # NIST K-283
                case "large":
                    curve = ec.SECT409K1() # NIST K-409
        case "nistk":
            match curv_size:
                case "small":
                    curve = ec.SECT163R2() # NIST B-163
                case "medium":
                    curve = ec.SECT283R1() # NIST B-283
                case "large":
                    curve = ec.SECT571R1() # NIST B-571

    private_key = ec.generate_private_key(curve)
    public_key = private_key.public_key()
    return private_key, public_key

if __name__=="__main__":
    KEY_SIZES=[1024,2048,4096]
    for key_size in KEY_SIZES:
        private_key, public_key = rsa_keygen(key_size)
        with open("../keys/"+str(key_size)+"_private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        with open("../keys/"+str(key_size)+"_public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    CURVES=["nistp","nistb","nistk"]
    SIZES=["small","medium","large"]
    for curve in CURVES:
        for size in SIZES:
            private_key, public_key = ec_keygen(curve,size)
            with open("../keys/"+curve+"_"+size+"_private_key.pem", "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                ))
            with open("../keys/"+curve+"_"+size+"_public_key.pem", "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
