package main

import "fmt"

func unshuffle(inp []byte, sbox []int) []byte {
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

func unfeistel_round(block []byte, sbox []int) []byte {
	if len(block) != EDES_BLOCK_SIZE {
		panic("Mismatched block size!")
	}
	left := block[:4]
	right := block[4:]
	outp := unshuffle(right, sbox)
	left = right
	right = make([]byte, 0)
	for i := 0; i < len(outp); i++ {
		right = append(right, outp[i]^left[i])
	}
	return append(left, right...)
}

func decrypt(password []byte, input_bytes []byte, print_to_stdout bool) []byte {
	// Generate the key schedule
	key := keygen(password, 32)
	sboxes := get_sboxes(key, false)
	// Split the input into blocks
	input_blocks := break_to_blocks(input_bytes)
	// Decrypt each block
	for round := 0; round < ROUND_NUM; round++ {
		for i := 0; i < len(input_blocks); i++ {
			input_blocks[i] = unfeistel_round(input_blocks[i], sboxes[round])
		}
	}
	// Join the blocks into a single byte slice
	decrypted := make([]byte, 0)
	for _, b := range input_blocks {
		decrypted = append(decrypted, b...)
	} // Print the output to stdout if requested
	ptext := unpad(string(decrypted))
	if print_to_stdout {
		fmt.Println(ptext)
	}

	return []byte(ptext)
}
