from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives.asymmetric import rsa


def sign_rsa_PSS(message, private_key):
    signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
    )

    return signature

def sign_rsa_PKCS1(message, private_key):
    signature = private_key.sign(
    message,
    padding.PKCS1v15(),
    hashes.SHA256()
    )

    return signature


