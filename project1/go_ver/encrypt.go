package main

import (
	"encoding/hex"
	"fmt"
	"os"
)

func shuffle(inp []byte, sbox []int) []byte {
	if len(inp) != 4 {
		panic("Mismatched block size!")
	}
	in0 := int(inp[0])
	in1 := int(inp[1])
	in2 := int(inp[2])
	in3 := int(inp[3])

	out0 := (in0 + in1 + in2 + in3) % 256
	out1 := (in0 + in1 + in2) % 256
	out2 := (in0 + in1) % 256
	out3 := in0

	out0 = sbox[out0]
	out1 = sbox[out1]
	out2 = sbox[out2]
	out3 = sbox[out3]

	out := []byte{byte(out0), byte(out1), byte(out2), byte(out3)}
	return out
}

func feistel_round(block []byte, sbox []int) []byte {
	if len(block) != EDES_BLOCK_SIZE {
		panic("Mismatched block size!")
	}
	left := block[:4]
	tmp := left
	right := block[4:]
	//fmt.Printf("left: %x, right: %x\n", left, right)
	outp := shuffle(right, sbox)
	//fmt.Printf("shuffled: %x\n", shuffled)
	left = right

	// make right empty byte slice
	right = make([]byte, 0)
	// xor the elements of outp and temp
	for i := 0; i < len(outp); i++ {
		right = append(right, outp[i]^tmp[i])
	}

	//fmt.Printf("xored: %x\n", xored)
	return append(left, right...)
}

func encrypt(password []byte, input_bytes []byte, print_to_stdout bool) []byte {
	// generate sboxes
	fmt.Println("2 Key: ", password)

	key := keygen(password, EDES_KEY_SIZE)

	sboxes := get_sboxes(key, print_to_stdout)

	input_blocks := break_to_blocks(input_bytes)

	//fmt.Println(sboxes)

	// pad input
	input := pad(input_blocks)

	// encrypt
	encrypted := make([]byte, 0)

	for tmp := 0; tmp < (16); tmp++ {
		for i := 0; i < (len(input)); i++ {

			input[i] = feistel_round(input[i], sboxes[tmp])
		}
	}

	for _, b := range input {
		encrypted = append(encrypted, b...)
	}
	return encrypted
}

func main() {
	// parse args from command line to get key
	key := []byte(os.Args[1])
	fmt.Println("1 Key: ", key)
	input_text := read_from_stdin()
	input_bytes := []byte(input_text)

	if len(os.Args) > 2 && os.Args[2] == "-des" {
		// encrypt with des
		print()
	} else {
		encrypted := hex.EncodeToString(encrypt(key, input_bytes, false))
		fmt.Print((encrypted))
		os.WriteFile("encrypted", []byte(encrypted), 0644)
	}
	fmt.Println("[-] Encrypted!")

}
