use std::net::SocketAddr;
use std::{vec, fs};

use p256::NistP256;
use rsa::{RsaPublicKey, RsaPrivateKey, pkcs1::DecodeRsaPublicKey, pkcs1::DecodeRsaPrivateKey   };
use rsa::pkcs1v15::{SigningKey, VerifyingKey};
use rsa::pss::{BlindedSigningKey, VerifyingKey as PSSVerifyingKey};
use rsa::signature::{RandomizedSigner, Signature, Verifier, Keypair};
use sha2::{Digest, Sha256};
use rsa::{ pkcs8::DecodePublicKey};



use p256::{
    ecdsa::{
        signature::{Signer, Verifier as ECVerifier},
        SigningKey as ECSigningKey, VerifyingKey as ECVerifyingKey,
    },
    pkcs8::EncodePrivateKey,
    PublicKey, SecretKey as p256SecretKey,
};

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

fn ec_load_nistp256_key()-> p256SecretKey {

        //nist p256
        
        let priv_filename = format!("../../keys/nistp_small_private_key.pem");

        let privk = fs::read_to_string(priv_filename).expect("Failed to Read file");









        let private_key = p256::SecretKey::from_sec1_pem(&privk).expect("Failed to read private key!");
        
    return private_key;
}

fn ec_perf() {
  
    let secret_key = ec_load_nistp256_key();

    // Derive public key
    let public_key = secret_key.public_key();


    // Signing
    let start = std::time::SystemTime::now();
    let signing_key: ECSigningKey = secret_key.into();
    let message = b"ECDSA proves knowledge of a secret number in the context of a single message";
    let signature = signing_key.sign(message);

    // Verification
    let verifying_key: ECVerifyingKey = public_key.into();
    let end = std::time::SystemTime::now();
    let duration = end.duration_since(start).expect("Time went backwards");
    println!("NIST P-256: {} ms", duration.as_millis());
    assert!(verifying_key.verify(message, &signature).is_ok());
}

fn main() {
    rsa_perf();
    ec_perf();
}
