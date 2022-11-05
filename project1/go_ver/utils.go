package main

import (
	"crypto/sha256"
	"fmt"
	"os"
	"strconv"

	"golang.org/x/crypto/pbkdf2"
	"golang.org/x/crypto/sha3"
)

const EDES_BLOCK_SIZE = 8
const EDES_KEY_SIZE = 32

func main() {
	// Only for testing purposes
	if len(os.Args) < 2 {
		fmt.Println("[!] Please provide a password!")
		os.Exit(1)
	}
	//	input := os.Args[1]
	//
	//	// Block separation test
	//	input_blocks := break_to_blocks(input)
	//	for _, block := range input_blocks {
	//		println(block)
	//	}
	//
	//	println("===========")
	//	// Padding Test
	//	input_blocks = pad(input_blocks)
	//	println("Padded input:")
	//	for _, block := range input_blocks {
	//		println(block)
	//	}
	//
	//	// Unpadding test
	//	output := strings.Join(input_blocks, "")
	//	output = unpad(output)
	//	println("Unpadded output: ", output)
	//

	// keygen test
	key := os.Args[2]
	//fmt.Printf("%x\n", key)
	//fmt.Printf("%x\n", key)

	//key_bytes := salt_key(keygen([]byte(key), EDES_KEY_SIZE))

	//fmt.Printf("%x\n", key_bytes)
	//fmt.Printf("%x\n", transform_key(key_bytes))
	key_B := transform_key(keygen([]byte(key), EDES_KEY_SIZE))
	test_sbox := generate_sbox([]byte(key_B))
	fmt.Printf("%x\n", test_sbox)
}

//Given a list of strings, pad the last one with bytes containing the number of characters needed to get to length of 8
//If the last string is already 8 characters, add a new string with 8 bytes of 8
func pad(input_blocks []string) []string {
	last_block_len := len(input_blocks[len(input_blocks)-1])
	last_block := input_blocks[len(input_blocks)-1]
	missing := 8 - last_block_len

	if missing == 0 {
		input_blocks = append(input_blocks, string([]byte{8, 8, 8, 8, 8, 8, 8, 8}))
		return input_blocks
	} else {
		for i := 0; i < missing; i++ {
			last_block += strconv.Itoa(missing)
		}
	}
	input_blocks[len(input_blocks)-1] = last_block
	return input_blocks
}

func unpad(inputText string) string {
	/* Unpads a string previously padded. Might work with bytes, idk */
	fmt.Println(inputText)

	toRemove_str := inputText[len(inputText)-1:]
	toRemove, err := strconv.Atoi(toRemove_str)
	if err != nil {
		fmt.Println("[!] Error unpadding!")
	}
	inputText = inputText[:len(inputText)-toRemove]
	return inputText
}

func read_from_stdin() string {
	var input string
	_, err := fmt.Scan(&input)
	if err != nil {
		fmt.Println("[!] Error reading input text!")
	}
	return input
}

// Go-original function
func break_to_blocks(input string) []string {
	input_blocks := []string{}
	for len(input) >= 8 {
		input_blocks = append(input_blocks, input[:8])
		input = input[8:]
	}
	input_blocks = append(input_blocks, input)
	return input_blocks
}

func keygen(pw []byte, len int) []byte {
	// Generate a key of len bytes from a password
	salt := []byte{0}
	key := pbkdf2.Key(pw, salt, 1, len, sha256.New)

	return key
}

func salt_key(key []byte) []byte {
	// Despite the name, this func is used to generate a unique name for the sbox file that does not give away the key used
	salt := 0
	//iterate over the individual bytes of the key
	for _, b := range key {
		salt += int(b)
	}
	keycopy := append(key, strconv.Itoa(salt)...)
	return keygen(keycopy, 32)
}

func transform_key(key []byte) []byte {
	key = append(key, byte(1))
	return key
}

func get_int_index(el int, searchlist []int) int {
	for i, b := range searchlist {
		if b == el {
			return i
		}
	}
	// error
	return -1
}

func generate_sbox(key []byte) []byte {
	// Derive key to get our seed
	fmt.Printf("%x\n\n", key)
	seedbox := make([]byte, 256)
	c1 := sha3.NewShake256()
	c1.Write(key)
	c1.Read(seedbox)
	// get a list of ints from a list of bytes with the values of these bytes

	seedbox_i := make([]int, len(seedbox))
	for i, b := range seedbox {
		seedbox_i[i] = int(b)
	}

	box := make([]int, 256)
	samplebox := make([]int, 256)

	for i := 0; i < 256; i++ {
		box[i] = i
		samplebox[i] = i
	}

	for i, b := range seedbox_i {
		// add index to element
		seedbox_i[i] = (b + i) % len(seedbox_i)
	}

	// this python code  for i in range(len(seedbox)):        samplebox=box        tmp=box[box.index(samplebox[i])]        box.remove(samplebox[i])        box.insert(seedbox[i],tmp)  in golang
	for i := 0; i < len(seedbox_i); i++ {
		samplebox = box
		original_pos := box[get_int_index(samplebox[i], box)]

		// remove element in index original_pos from box
		box = append(box[:original_pos], box[original_pos+1:]...)
		fmt.Println(box)

	}
	fmt.Println(box)
	return nil
}

func get_sboxes(key []byte, print_to_stdout bool) {
	// declare empty 2 dimensional array

	return

}
