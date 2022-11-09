package main

import (
	"bufio"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"

	"golang.org/x/crypto/pbkdf2"
	"golang.org/x/crypto/sha3"
)

const EDES_BLOCK_SIZE = 8
const EDES_KEY_SIZE = 32
const SBOX_PATH = "sboxes/"
const ROUND_NUM = 16

func test_main() {
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
	key_B := keygen([]byte(key), EDES_KEY_SIZE)
	//test_sbox := generate_sbox([]byte(key_B))
	get_sboxes(key_B, false)
	//fmt.Printf("%x\n", test_sbox)
}

//Given a list of strings, pad the last one with bytes containing the number of characters needed to get to length of 8
//If the last string is already 8 characters, add a new string with 8 bytes of 8
func pad(input_blocks [][]byte) [][]byte {
	last_block_len := len(input_blocks[len(input_blocks)-1])
	last_block := input_blocks[len(input_blocks)-1]
	missing := 8 - last_block_len
	if missing == 0 {
		input_blocks = append(input_blocks, []byte{8, 8, 8, 8, 8, 8, 8, 8})

		return input_blocks
	} else {
		for i := 0; i < missing; i++ {
			last_block = append(last_block, strconv.Itoa(missing)...)
		}
	}
	input_blocks[len(input_blocks)-1] = last_block
	return input_blocks
}

func unpad(inputText []byte) []byte {
	/* Unpads a string previously padded. Might work with bytes, idk */
	toRemove_str := inputText[len(inputText)-1:]
	toRemove, err := strconv.Atoi(string(toRemove_str))
	if err != nil {
		panic("[!] Could not unpad!")
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

func break_to_blocks(input []byte) [][]byte {
	input_blocks := [][]byte{}
	for len(input) >= 8 {
		input_blocks = append(input_blocks, input[:8])
		input = input[8:]
	}
	if len(input) > 0 {
		input_blocks = append(input_blocks, input)
	}
	return input_blocks
}

func keygen(pw []byte, len int) []byte {
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
	//salt = salt - 1 // for consistency with the python version, which doesnt add the null byte at the end :)
	keycopy := append(key, strconv.Itoa(salt)...)
	a := keygen(keycopy, 32)
	return a
}

func transform_key(key []byte) []byte {
	key = append(key, byte(1))
	key = keygen(key, 32)
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

func generate_sbox(key []byte) []int {
	// Derive key to get our seed
	//fmt.Printf("%x\n\n", key)
	seedhash := make([]byte, 256)
	c1 := sha3.NewShake256()
	c1.Write(key)
	c1.Read(seedhash)
	// get a list of ints from a list of bytes with the values of these bytes

	seedbox := make([]int, len(seedhash))
	for i, b := range seedhash {
		seedbox[i] = int(b)
	}

	box := make([]int, 256)

	for i := 0; i < 256; i++ {
		box[i] = i
	}

	for i, b := range seedbox {
		// add index to element
		seedbox[i] = (b + i) % len(seedbox)
	}

	// declare a list of pairs of ints called shuffles
	shuffle_pairs := make([][2]int, 0)

	for i := 0; i < len(seedbox); i++ {
		shuffle_pairs = append(shuffle_pairs, [2]int{seedbox[i], box[i]})
	}

	// sort the list of pairs by the first element of each pair
	sort.Slice(shuffle_pairs, func(i, j int) bool {
		if shuffle_pairs[i][0] != shuffle_pairs[j][0] {
			return shuffle_pairs[i][0] < shuffle_pairs[j][0]
		} else if shuffle_pairs[i][0] == shuffle_pairs[j][0] {
			return shuffle_pairs[i][1] < shuffle_pairs[j][1]
		}
		panic("THIS SHOULD NOT HAPPEN")
		return false
	})

	// get the second element of each pair and put it in a new list
	shuffled_box := make([]int, len(shuffle_pairs))
	for i, pair := range shuffle_pairs {
		shuffled_box[i] = pair[1]
	}
	//fmt.Println(seedbox)
	//fmt.Println(shuffle_pairs)

	return shuffled_box
}

func get_sboxes(key []byte, print_to_stdout bool) [][]int {
	sboxes := make([][]int, 0)
	new_pass := salt_key(key)

	filename_box := hex.EncodeToString(new_pass)

	boxpath := SBOX_PATH + filename_box

	if _, err := os.Stat(SBOX_PATH); os.IsNotExist(err) {
		err := os.Mkdir(SBOX_PATH, os.ModePerm)
		if err != nil {
			log.Println(err)
		}
	}

	// check if the file exists
	if _, err := os.Stat(boxpath); os.IsNotExist(err) {
		// file does not exist
		if print_to_stdout {
			fmt.Println("[-] No sboxes found. Creating..")
		}
		ret_sboxes := make([][]int, 0)
		keycopy := key
		for i := 0; i < ROUND_NUM; i++ {
			keycopy = transform_key(keycopy)
			//fmt.Println("Keycopy: ", keycopy)
			ret_sboxes = append(ret_sboxes, generate_sbox(keycopy))
		}

		// write the sboxes to a file
		file, err := os.Create(boxpath)
		if err != nil {
			fmt.Println("[!] Error creating sbox file!")
			fmt.Println(err)
		}
		defer file.Close()

		for _, sbox := range ret_sboxes {
			for i, el := range sbox {
				if i == len(sbox)-1 {
					file.WriteString("0x" + strconv.FormatInt(int64(el), 16))
				} else {
					file.WriteString("0x" + strconv.FormatInt(int64(el), 16) + ", ")
				}
			}
			file.WriteString("\n")
		}
		file.Sync()
		sboxes = ret_sboxes
	} else {
		// file exists
		if print_to_stdout {
			fmt.Println("[-] Sboxes found! Importing..")
		}
		file, err := os.Open(boxpath)
		if err != nil {
			fmt.Println("[!] Error opening sbox file!")
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()
			sbox := make([]int, 0)
			for _, el := range strings.Split(line, ", ") {
				if el != "" {
					// remove the 0x
					el = el[2:]
					el_int, err := strconv.ParseInt(el, 16, 64)

					if err != nil {
						fmt.Println("[!] Error converting sbox element to int!")
					}
					sbox = append(sbox, int(el_int))
				}
			}
			sboxes = append(sboxes, sbox)
		}
	}

	//if print_to_stdout {
	//	for i, sbox := range sboxes {
	//		fmt.Println("Sbox", i)
	//		fmt.Println(sbox)
	//	}
	//}
	return sboxes

}
