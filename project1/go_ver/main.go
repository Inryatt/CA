package main

import (
	"encoding/hex"
	"flag"
	"fmt"
	"os"
	"time"
)

func main() {
	// parse args from command line to get key
	//
	//fmt.Println("1 Key: ", key)
	input_text := read_from_stdin()

	dec := flag.Bool("d", false, "decrypt")
	enc := flag.Bool("e", false, "encrypt")
	speed_flag := flag.Bool("s", false, "measure speed")

	flag.Parse()
	args := flag.Args()

	key := []byte(args[0])
	if *speed_flag {
		if len(args) != 1 {
			panic("Usage: go_ver -s des/edes")
		}
		des := false
		edes := false
		for _, arg := range args {
			if arg == "des" {
				des = true
			} else if arg == "edes" {
				edes = true
			}
		}
		if !des && !edes {
			panic("Usage: go_ver -s des/edes")
		}
		speed(des, edes)
		return
	}
	if *dec && *enc {
		fmt.Println("[-] Error: both -d and -e flags set!")
		print_usage()
	}
	if *dec {
		fmt.Println("[-] Decrypting...")
		fmt.Println([]byte(input_text))
		input_bytes, err := hex.DecodeString(input_text)
		fmt.Println("Input bytes: ", input_bytes)
		if err != nil {
			panic("[!] Error decoding input text!")
		}
		decrypted := decrypt(key, input_bytes, true)
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

func speed(des bool, edes bool) {
	buffer := urandom(4096)

	if edes {
		edes_time := []int{}
		for i := 0; i < 100; i++ {
			key := urandom(20)
			start := time.Now()
			encrypted := encrypt(key, buffer, false)
			decrypted := decrypt(key, encrypted, false)
			end := time.Now()
			if decrypted != buffer {
				panic("[!] Something failed here!")
			}
			edes_time = append(edes_time, int(end.Sub(start).Milliseconds()))
		}
		// get minimum value in edes_time
		min := edes_time[0]
		for _, v := range edes_time {
			if v < min {
				min = v
			}
		}
		fmt.Println(min)
	}
	if des {
		// pass
	}
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func urandom(size int) []byte {
	size_byte := make([]byte, size, size)
	f, err := os.Open("/dev/urandom")
	check(err)
	n, err := f.Read(size_byte)
	fmt.Println(size_byte)
	if len(size_byte) != n || err != nil {
		panic("Error reading urandom")
	}
	check(err)
	f.Close()

	return size_byte
}
