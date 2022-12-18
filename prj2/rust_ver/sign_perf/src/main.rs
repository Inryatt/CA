use std::vec;

use rsa::{RsaPublicKey, RsaPrivateKey, pkcs1::DecodeRsaPublicKey, pkcs1::DecodeRsaPrivateKey   };
use rsa::pkcs1v15::{SigningKey, VerifyingKey};
use rsa::signature::{RandomizedSigner, Signature, Verifier};
use sha2::{Digest, Sha256};

// list with key sizes
fn rsa_load_keys()-> Vec<(RsaPublicKey, RsaPrivateKey)> {
    let key_size = vec![1024, 2048, 4096];
    let mut keys = vec![];

    for size in key_size {
        let pub_filename = format!("../../keys/{}_public_key.pem", size);
        let pubkey = std::fs::read_to_string(pub_filename).unwrap();
        let public_key = RsaPublicKey::from_pkcs1_pem(&pubkey).expect("Failed to read public key!");
        
        let priv_filename = format!("../../keys/{}_private_key.pem", size);
        let privkey = std::fs::read_to_string(priv_filename).unwrap();
        let private_key = RsaPrivateKey::from_pkcs1_pem(&privkey).expect("Failed to read private key!");
        
        let keypair = (public_key, private_key);
        keys.push(keypair);
    }
    return keys;
}

fn rsa_perf(){
    let KEYS = rsa_load_keys();
    for keypair in KEYS{
        let (public_key, private_key) = keypair;
        let signing_key = SigningKey::<Sha256>::new_with_prefix(private_key);
        let verifying_key: VerifyingKey<_> = (&signing_key).into();
    }
        
}

fn main() {
    rsa_perf()
}
