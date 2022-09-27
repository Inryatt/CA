import sys
import time
import math

menu="""
[1] - Count Characters
[2] - Count N-Grams
[3] - Exit
"""

def readfile(filename):
    """Read file :)"""
    with  open(filename,"r") as f:
        lines = f.readlines()
    out=""
    for line in lines:
        out+=line
    return out

def countchars(out):
    """Get count of characters in text"""
    chars={}
    # Single character occurrence
    for ch in out:
        chars[ch] = chars[ch]+1 if ch in chars else 1

    
    return chars

def analyze(rawdict:dict,totalchars:int):
    sort = sorted(rawdict.items(), key = lambda x:x[1], reverse=True)
    MULTIPLIER = (1/(sort[0][1]/totalchars))*10
    print(f"key: \ncharacter(s) : nº occurrences : percentage ")

    for it in sort[:100]:
        perc=(it[1]/totalchars)
        n=0
        print(f"{it[0]} :{it[1]:7} :{perc*100:10.3}%  "+("".join(["=" for n in range(0,int(math.log(perc*MULTIPLIER,2)*10))])))
  
def countngrams(n,out):
    """Get a count of the ngrams in text"""
    ngrams={}

    # N-Gram
    while len(out)>(n-1):
        ngrams[out[:n]] =ngrams[out[:n]]+1  if out[:n] in ngrams else 1

        out=out[1:]
    return ngrams

def main():
    print("Howdy!")
    filen=sys.argv[1]
    out = readfile(filen)
    totalchar = len(out)
    chars = ""
    ngrams= ""
    try:
        while True:
            print(menu)
            inp =input("Select: ")
            match inp:
                case "1":
                    if chars=="":
                        start_time = time.time()
                        chars = countchars(out)
                        print("--- %s seconds ---" % (time.time() - start_time))
                    print("===== Per Character Stats =====")
                    analyze(chars,totalchar)
                    #print(chars)
                case "2":
                    n =input("Value of n? ")
                    try:
                        n= int(n)
                        if n>totalchar or n<2:
                            raise Exception
                        start_time = time.time()

                        ngrams = countngrams(n,out)
                        print("--- %s seconds ---" % (time.time() - start_time))
                        analyze(ngrams,totalchar/n)
                        #print(ngrams)
                    except:
                        print(f"Please input a number between 2-{totalchar}")
                case "3":
                    raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nBye :)")
        return 0
                
main()
