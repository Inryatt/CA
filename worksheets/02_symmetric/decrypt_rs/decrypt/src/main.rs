extern crate crypto;

use std::fs;
use std::env;
use crypto::aes::{mod, KeySize};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len()<4 {
        println!("Usage: cargo run -- <key> <file to decrypt> <output file>")
    }

    let key = fs::read_to_string(&args[1])
        .expect("Couldnt read key");


    println!("key: \n{key}");
}
