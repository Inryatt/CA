use std::vec;

use rsa::{RsaPublicKey, RsaPrivateKey, pkcs1::DecodeRsaPublicKey, pkcs1::DecodeRsaPrivateKey   };
use rsa::pkcs1v15::{SigningKey, VerifyingKey};
use rsa::pss::{BlindedSigningKey, VerifyingKey as PSSVerifyingKey};
use rsa::signature::{RandomizedSigner, Signature, Verifier, Keypair};
use sha2::{Digest, Sha256};
use rsa::{ pkcs8::DecodePublicKey};


// list with key sizes
fn rsa_load_keys()-> Vec<(RsaPrivateKey)> {
    let key_size = vec![1024, 2048, 4096];
    let mut keys = vec![];

    for size in key_size {
       let priv_filename = format!("../../keys/{}_private_key.pem", size);
        let private_key = RsaPrivateKey::read_pkcs1_pem_file(&priv_filename).expect("Failed to read private key!");
        
        keys.push(private_key);
    }
    return keys;
}


fn rsa_perf(){

    // PKCS1
    let mut rng = rand::thread_rng();
    let keys = rsa_load_keys();
    for keypair in keys{
        let (private_key) = keypair;      
        let signing_key = SigningKey::<Sha256>::new(private_key);
        let verifying_key: VerifyingKey<_> = (&signing_key).into();    


        // get unix timestamp
        let start = std::time::SystemTime::now();
        let data = b"this is a message";
        let signature = signing_key.sign_with_rng(&mut rng, data);
        verifying_key.verify(data, &signature).expect("[!] - failed to verify!!");
        let end = std::time::SystemTime::now();
        let duration = end.duration_since(start).expect("Time went backwards");
        println!("PKCS1: {} ms", duration.as_millis());

    }
    //PSS

    let keys = rsa_load_keys();
    for keypair in keys{
        let ( private_key) = keypair;      
        let signing_key = BlindedSigningKey::<Sha256>::new(private_key);
        let verifying_key: PSSVerifyingKey<_> = (&signing_key).into();    


        // get unix timestamp
        let start = std::time::SystemTime::now();
        let data = b"this is a message";
        let signature = signing_key.sign_with_rng(&mut rng, data);
        verifying_key.verify(data, &signature).expect("[!] - failed to verify!!");
        let end = std::time::SystemTime::now();
        let duration = end.duration_since(start).expect("Time went backwards");
        println!("PSS: {} ms", duration.as_millis());
    }
        
}

fn main() {
    rsa_perf()
}
