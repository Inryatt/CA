from tabnanny import check
from makehash import makehash

def getcollision() -> int:
    c=0
    while True:
        # Generate new hash
        c+=1
        hash = makehash()[:5]
        
        if checkcollision(hash):
            break
        
        # store in file
        with open("paradox_hashes", "a+b") as f:
            f.write(hash+b"\n")
    print(f"Found a collision after {c} tries! :)")
    return c


def checkcollision(newhash:bytes)->bool:
    with open("paradox_hashes", "r+b") as f:
        hashes = f.readlines()
    for hash in hashes:
       if newhash==hash.strip():
        return True
            
    return False

def main():
    try:
        with open("paradox_hashes", "r+b") as f:
            pass
    except:
        with open("paradox_hashes", "w+b") as f:
            pass
    numattempts=[]
    for i in range(10):
        numattempts.append(getcollision())
    print(numattempts)

main()