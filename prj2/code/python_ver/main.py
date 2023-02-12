import sys
import keygen
import sign
import verify


def main():
    chosen_algorithm = sys.argv[1]
    match chosen_algorithm.lower():
        case "rsa":
            chosen_algorithm="rsa"
        case "el":
            chosen_algorithm="el"
        

