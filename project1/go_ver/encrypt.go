package main

import (
	"crypto/des"
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

	outp := shuffle(right, sbox)
	left = right
	right = make([]byte, 0)
	for i := 0; i < len(outp); i++ {
		right = append(right, outp[i]^tmp[i])
	}

	return append(left, right...)
}

func encrypt(password []byte, input_bytes []byte, print_to_stdout bool) []byte {

	key := keygen(password, EDES_KEY_SIZE)
	sboxes := get_sboxes(key, print_to_stdout)
	input_blocks := break_to_blocks(input_bytes)

	input := pad(input_blocks)

	encrypted := make([]byte, 0)

	for tmp := 0; tmp < 16; tmp++ {

		for i := 0; i < len(input); i++ {
			input_copy := make([]byte, len(input[i]))
			copy(input_copy, input[i])
			input[i] = feistel_round(input_copy, sboxes[tmp])

		}
	}

	for _, b := range input {
		encrypted = append(encrypted, b...)
	}
	return encrypted
}

// Encrypt using single DES (not EDES)

func des_encrypt(key []byte, input_bytes []byte) []byte {
	key = keygen(key, 8)
	cipher, err := des.NewCipher(key)
	if err != nil {
		panic(err)
	}

	ciphertext := []byte{}
	input_blocks := break_to_blocks(input_bytes)
	input_blocks = des_pad(input_blocks)

	for {
		if len(input_blocks) > 1 {
			block := make([]byte, 8)
			copy(block, input_blocks[0])

			input_blocks = input_blocks[1:]
			tmp := make([]byte, 8)

			cipher.Encrypt(tmp, block)
			ciphertext = append(ciphertext, tmp...)

		} else if len(input_blocks) == 1 {
			txt := make([]byte, 8)
			copy(txt, input_blocks[0])

			tmp := make([]byte, 8)
			cipher.Encrypt(tmp, txt)
			ciphertext = append(ciphertext, tmp...)
			break
		}

	}
	return ciphertext
}
