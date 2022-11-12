package main

import (
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"os"
	"time"
)

func main() {
	// parse args from command line to get key
	//
	//fmt.Println("1 Key: ", key)

	dec := flag.Bool("d", false, "decrypt")
	enc := flag.Bool("e", false, "encrypt")
	speed_flag := flag.Bool("s", false, "measure speed")
	des := flag.Bool("des", false, "use DES ")
	flag.Parse()
	args := flag.Args()

	key := []byte(args[0])
	if *speed_flag {
		if len(args) < 1 || len(args) > 2 {
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
		os.Exit(0)
	}
	input_text := read_from_stdin()

	if *dec && *enc {
		fmt.Println("[-] Error: both -d and -e flags set!")
		print_usage()
	}

	if *dec {
		fmt.Println("[-] Decrypting...")
		fmt.Println(input_text)
		input_bytes, err := hex.DecodeString(input_text)
		fmt.Println("Input bytes: ", input_bytes)
		if err != nil {
			panic("[!] Error decoding input text!")
		}
		var decrypted []byte
		if *des {
			decrypted = des_decrypt(key, input_bytes)
		} else {
			decrypted = decrypt(key, input_bytes, true)
		}
		fmt.Println("[!] Decrypted!")
		fmt.Println("[-] Output: ", string(decrypted))
		return
	}

	if *enc {

		fmt.Println("[-] Encrypting...")
		input_bytes := []byte(input_text)
		var encrypted string
		if *des {
			encrypted = hex.EncodeToString(des_encrypt(key, input_bytes))
		} else {
			encrypted = hex.EncodeToString(encrypt(key, input_bytes, false))
		}
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
		edes_time := []float32{}
		for i := 0; i < 1000; i++ {
			key := urandom(20)
			start := time.Now()
			encrypted := encrypt(key, buffer, false)
			decrypted := decrypt(key, encrypted, false)
			end := time.Now()
			//if decrypted != buffer {
			//	panic("[!] Something failed here!")
			//}
			decrypted = decrypted
			edes_time = append(edes_time, float32(end.Sub(start).Seconds()))
		}
		// get minimum value in edes_time
		min := edes_time[0]
		for _, v := range edes_time {
			if v < min {
				min = v
			}
		}
		fmt.Printf("%fs\n", min)
	}
	if des {
		des_time := []float32{}
		for i := 0; i < 100000; i++ {
			key := urandom(20)
			start := time.Now()
			encrypted := des_encrypt(key, buffer)
			decrypted := des_decrypt(key, encrypted)
			end := time.Now()
			//if !cmp.Equal(decrypted, buffer) {
			//	panic("[!] Something failed here!")
			//}
			//fmt.Println(buffer[:100])
			//fmt.Println(decrypted[:100])
			//fmt.Println("==========")
			decrypted = decrypted
			des_time = append(des_time, float32(end.Sub(start).Seconds()))
		}
		// get minimum value in edes_time
		min := des_time[0]
		for _, v := range des_time {
			if v < min {
				min = v
			}
		}
		fmt.Printf("%fs\n", min)
	}
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func urandom(size int) []byte {
	size_byte := make([]byte, size)
	f, err := os.Open("/dev/urandom")
	check(err)
	n, err := io.ReadFull(f, size_byte)
	if len(size_byte) != n || err != nil {
		panic("Error reading urandom")
	}
	check(err)
	f.Close()

	return size_byte
}
