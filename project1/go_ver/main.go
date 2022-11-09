package main

import (
	"encoding/hex"
	"flag"
	"fmt"
	"os"
)

func main() {
	// parse args from command line to get key
	key := []byte(os.Args[1])
	//fmt.Println("1 Key: ", key)
	input_text := read_from_stdin()

	dec := flag.Bool("d", false, "decrypt")
	enc := flag.Bool("e", false, "encrypt")

	flag.Parse()

	if *dec && *enc {
		fmt.Println("[-] Error: both -d and -e flags set!")
		print_usage()

	}
	if *dec {
		fmt.Println("[-] Decrypting...")
		input_bytes, err := hex.DecodeString(input_text)
		if err != nil {
			panic("[!] Error decoding input text!")
		}
		decrypted := decrypt(input_bytes, key, true)
		fmt.Println("[!] Decrypted!")
		fmt.Println("[-] Output: ", string(decrypted))
		return
	}
	if *enc {
		fmt.Println("[-] Encrypting...")
		input_bytes := []byte(input_text)

		encrypted := hex.EncodeToString(encrypt(key, input_bytes, false))
		fmt.Println("[-] Encrypted!")
		fmt.Println("[-] Output: ", string(encrypted))

		os.WriteFile("encrypted", []byte(encrypted), 0644)
		return
	}
	fmt.Println("[!] Error: no flags set!")
	print_usage()
}

func print_usage() {
	fmt.Println("Usage: <content_to_decrypt> | go run main.go -d/-e <text_key> ")
	fmt.Println("To use DES, append -des to the previous command.")
	//fmt.Println("Hint: If you encrypted, you can do:")
	//fmt.Println("echo encrypted | go run main.go <key> -d")
	os.Exit(1)
}
