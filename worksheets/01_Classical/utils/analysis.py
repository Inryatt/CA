from operator import ne
import re
import sys
import time
import math
from unittest import result

menu="""
[0] - Exit
[1] - Count Characters
[2] - Count N-Grams
[3] - Find Repeated (Kasiski's Method)
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

def analyze(rawdict:dict,totalchars:int, outputlen=100):
    sort = sorted(rawdict.items(), key = lambda x:x[1], reverse=True)
    MULTIPLIER = (1/(sort[0][1]/totalchars))*10
    print(f"key: \ncharacter(s) : nº occurrences : percentage ")

    for it in sort[:outputlen]:
        perc=(it[1]/totalchars)
        n=0
        print(f"{it[0]} :{it[1]:7} :{perc*100:10.3}%  "+("".join(["=" for n in range(0,int(math.log(perc*MULTIPLIER,2)*10))])))

def kasiski_analyze(rawdict:dict,outputlen=100):
    """Display results for kasiski's method"""
    sort = sorted(rawdict.items(), key = lambda x:x[1][0], reverse=True)
    for it in sort[:outputlen]:
        print(it)

def countngrams(n,out):
    """Get a count of the ngrams in text"""
    ngrams={}
    if n==0:
        raise Exception # no
    # N-Gram
    while len(out)>(n-1):
        ngrams[out[:n]] =ngrams[out[:n]]+1  if out[:n] in ngrams else 1

        out=out[1:]
    return ngrams

def kasiski_distance(substr,text):
    #print(f"searching for {substr}")
    distance = {}
    #while len(text)>len(inp)-1:
     #   distance
    result = [_.start() for _ in re.finditer(substr, text)] 
    for i in range(0,len(result)-1,2):
        d = result[i+1]-result[i]
        distance[d] = distance[d]+1 if d in distance else 1
    #print(distance)
    return distance

# 4.1 - Finding key length for vignère
def kasiski(inp, maxsize, totalchars):
    """Find repeated bits of cryptogram"""
    result = {} # size, [num, elements...]
    step = int(10/maxsize)
    for i in range(2,maxsize+1):
        #print(f"["+("".join(["=" for n in range(1,step*i)]))+"".join(["-" for m in range(i,0,-1)])+"]")
        print(f"{(i/maxsize)*100-10}%",end='\r')
        out=countngrams(i,inp)
        for gram in  sorted(out.items(), key = lambda x:x[1], reverse=True)[:5]:
            dist = kasiski_distance(gram[0],inp)
            for el in dist.keys():
                if el in result.keys():
                    result[el][0]+=dist[el]
                    result[el][1]+=[gram[0]]
                else:
                    result[el]=[1,[gram[0]]]
    #factorize
    # https://stackoverflow.com/questions/43129076/prime-factorization-of-a-number
    # too mathy
    result = sorted(result.items(), key = lambda x:x[1][0], reverse=True)
    distances = [x[0] for x in result]
    #print(distances)
    factors = []
    for num in distances:
        tmp = []
        i=2
        while i < num:
            if (num %i ) ==0:
                if i not in tmp:
                    tmp.append(i)
                num = num/i
            else:
                i+=1
        factors.append(tmp)
    c=0
    factors_count={}
    for i in factors:
        for j in i:
            factors_count[j] = factors_count[j]+1 if  j in factors_count else 1
    factors_count = sorted(factors_count.items(), key = lambda x:x[1], reverse=True)
    #print(factors_count)
    keysize = factors_count[0][0]*factors_count[1][0]
    print(f"Most likely key size? {keysize}")

    return keysize
        #analyze(out,totalchars, outputlen=10)


def kasiski_parse(keysize,text) ->list[str]:
    results=[]
    for j in range(0,keysize):
        newtext=""

        for i in range(j,len(text),j+1):
            newtext+=text[i]
        results.append(newtext)
    return results

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
                            raise 
                        start_time = time.time()

                        ngrams = countngrams(n,out)
                        print("--- %s seconds ---" % (time.time() - start_time))
                        analyze(ngrams,totalchar/n)
                        #print(ngrams)
                    except:
                        print(f"Please input a number between 2-{totalchar}")
                case "3":
                  #  try:
                        maxs = int(input("Search until which size? "))
                        if maxs>totalchar or maxs<2:
                            raise IndexError
                        
                        keysize =kasiski(out,maxs,totalchar)
                        newtexts = kasiski_parse(keysize,out)
                        print(len(newtexts))
                        try:
                            while True:
                                try:
                                    print("To go back to main menu, Ctrl-C.")
                                    text_picked = int(input(f"Analyze which segment? (Pick a number between 1-{keysize} : "))-1
                                    size_picked= int(input(f"Size of n-grams? (Pick between 1-{len(newtexts[text_picked])}) : "))
                                    if text_picked>=0 and text_picked<keysize+2 and size_picked>0 and size_picked<len(newtexts[text_picked]):
                                        analyze(countngrams(size_picked,newtexts[text_picked]),len(newtexts[text_picked]))
                                except  Exception:
                                    print("Invalid input")
                        except KeyboardInterrupt:
                            continue
                        #kasiski_analyze(results)
                   # except IndexError:
                   #     print(f"Please input a number between 2-{totalchar}")
                case "0":
                    raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nBye :)")
        return 0
                
main()
