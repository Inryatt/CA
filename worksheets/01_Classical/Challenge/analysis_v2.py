from email.mime import base
from operator import ne, pos
import re
import sys
import time
import math
from typing import final
from unittest import result
from xml.etree.ElementPath import findtext

menu="""
[0] - Exit
[1] - Count Characters
[2] - Count N-Grams
[3] - Find Repeated (Kasiski's Method)
[4] - Attempt to break Vignére cipher
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

def analyze(rawdict:dict,totalchars:int, outputlen=100,exportfile=""):
    sort = sorted(rawdict.items(), key = lambda x:x[1], reverse=True)
    MULTIPLIER = (1/(sort[0][1]/totalchars))*10
    if exportfile=="":
        print(f"key: \ncharacter(s) : nº occurrences : percentage ")
        
        for it in sort[:outputlen]:
            perc=(it[1]/totalchars)
            n=0
            print(f"{it[0]} :{it[1]:7} :{perc*100:10.3}%  "+("".join(["=" for n in range(0,int(math.log(perc*MULTIPLIER,2)*10))])))
    else:
        with open(exportfile,"a") as f:
            f.write(f"key: \ncharacter(s) : nº occurrences : percentage \n")
            for it in sort[:outputlen]:
                perc=(it[1]/totalchars)
                n=0
                f.write(f"{it[0]} :{it[1]:7} :{perc*100:10.3}%  "+("".join(["=" for n in range(0,int(math.log(perc*MULTIPLIER,2)*10))]))+"\n")


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
        while not i > num:
            if (num % i ) ==0:
                if i not in tmp:
                    tmp.append(i)            
            i+=1
        factors.append(tmp)

   
    c=0
    factors_count={}
    for i in factors:
        for j in i:
            factors_count[j] = factors_count[j]+1 if  j in factors_count else 1
    factors_count = sorted(factors_count.items(), key = lambda x:x[1], reverse=True)
    #print(factors_count)
    factors = factors_count[0][0]*factors_count[1][0]
    #print(f"Most likely key size? {keysize}")

    return factors_count
        #analyze(out,totalchars, outputlen=10)


def kasiski_parse(keysize,text) ->list[str]:
    results=[]
    for j in range(0,keysize):
        newtext=""

        for i in range(j,len(text),keysize):
            newtext+=text[i]
        results.append(newtext)

    #for t in results:
    #    print(t[:50])
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
                        
                        key_factors =kasiski(out,maxs,totalchar)
                        done = False
                        #try:
                        try:
                                key=input(f"These are the factors that probably give the key size: {key_factors}\nTo test all, press 0 Otherwise, type in the value you think it is.\n")
                                keys =[]
                                print(f"key: {key}")
                                match key:
                                    case "0":
                                        done = True
                                        keys = [x[0] for x in key_factors]
                                        for key in keys:
                                            if key<maxs:
                                                newtexts = kasiski_parse(key,out)
                                                #print(len(newtexts))
                                                with open("export.txt","a") as f:
                                                    f.write(f"======Test for key size: {key}======\n")
                                                for text in newtexts:
                                                     analyze(countngrams(1,text),len(text),exportfile="export.txt")

                                        break
                                    case _:
                                        try:
                                            keys=int(key)
                                            keysize=keys
                                        except ValueError:
                                            print("Error : Invalid value")
                                            continue
                                if not done:
                                    newtexts = kasiski_parse(keysize,out)
                                    print(len(newtexts))
                                #except  Exception:
                                #    print("Invalid input")
                                if not done:    
                                    while True:
                                        print("To go back to main menu, Ctrl-C.")
                                        text_picked = int(input(f"Analyze which segment? (Pick a number between 1-{keysize} : "))-1
                                        size_picked= int(input(f"Size of n-grams? (Pick between 1-{len(newtexts[text_picked])}) : "))
                                        if text_picked>=0 and text_picked<keysize+2 and size_picked>0 and size_picked<len(newtexts[text_picked]):
                                            analyze(countngrams(size_picked,newtexts[text_picked]),len(newtexts[text_picked]))
                                
                        except KeyboardInterrupt:
                            continue
                        #kasiski_analyze(results)
                   # except IndexError:
                   #     print(f"Please input a number between 2-{totalchar}")
                case "4":
                    print("Experimental!")
                    maxs = int(input("Search until which size? "))
                    if maxs>totalchar or maxs<2:
                        raise IndexError
                    
                    key_factors =kasiski(out,maxs,totalchar)
                    key=input(f"These are the factors that probably give the key size: {key_factors}\nTo test all, press enter. Otherwise, type in the value you think it is.\n")
                    keys =[]
                    match key:
                        case "":
                            keys = [x for x in key_factors]
                            print("WIP.")
                            continue
                        case _:
                            try:
                                keys=int(key)
                                keysize=keys
                            except ValueError:
                                print("Error : Invalid value")
                                continue
                    newtexts = kasiski_parse(keysize,out)
                    #print(len(newtexts))
                    i=0
                    lang =None
                    alphabets =[
                        ['a','i','n','t','e','s','k','l','o','u','m','h','v','r','j','p','y','d','g','f','b','c','z','ERR','ERR','ERR'],
                        ['e','t','o','n','a','i','s','r','h','l','d','c','g','u','m','f','y','w','p','b','k','v','z','x','j','q'],
                        ['a','e','o','s','r','i','d','n','m','u','t','c','l','p','v','h','g','b','f','q','z','j','x','y','k','w'],
                    ]
                    newertexts=[]
                    possible_keys=[]
                    for text in newtexts:
                        if i ==0:
                            inp =input("Do you know the language of the original message? y/n\n")
                            match inp:
                                case "y":
                                    inp = input("WIP\n[1] - Finnish\n[2] - English\n[3] - Portuguese\n")
                                    match inp:
                                        case "1":
                                            lang = 0
                                        case "2":
                                            lang = 1
                                        case "3":
                                            lang = 2
                                        case _:
                                            print("Invalid input!")
                                            raise Exception
                                case "n":
                                    print("Too bad. (Coming Soon!)")
                                    raise Exception
                                case _:
                                    print("Invalid input.")
                                    raise Exception

                        res = countngrams(1,text)
                        res= sorted(res.items(), key = lambda x:x[1], reverse=True)

                        sumres=0
                        for p in res:
                            sumres+=p[1]
                        indecision=[]
                        res = [(pair[0],pair[1],round(((pair[1]/sumres)*100),2)) for pair in res]
                        #for i in range(0,len(res)-2):
                        #    if res[i][2]-res[i+1][2]<0.1:
                        #        indecision.append((res[i],res[i+1]))
                        #print(indecision)
                        print(res)
                        if res[0][2]-res[1][2]<0.2:
                            possible_keys.append((res[0][0],res[1][0]))
                        else:
                            possible_keys.append(res[0][0])
                        
                        #for i in range(len(res)-1):
                        #    print(f"{res[i][0]} becomes {alphabets[lang][i]}")
                        #newtext=""
                        #for j in range(0,len(text)-1):
                        #    #with open("log.txt","w+") as f:
                        #    #    f.write(f"{res[j][0]} becomes {alphabets[lang][j]}\n")
                        #    
                        #    index=None
                        #    for k in range(0,len(res)-1):                                
                        #        if res[k][0] == text[j]:
                        #            index = k
                        #            break
                        #   
                        #    newtext+=alphabets[lang][k]

                        #newertexts.append(newtext)
                        i+=1
                    print(possible_keys)
                    base_key = [x[0] for x in possible_keys]
                    
                    final_possible_keys=["".join(base_key)]

                    for i in range(len(possible_keys)):
                        if len(possible_keys[i])!=1:
                            for j in range(0,len(possible_keys[i])):
                                print(possible_keys[i][j])
                                tmp = base_key
                                tmp[i]=possible_keys[i][j]
                                print("".join(tmp))
                                if "".join(tmp) not in final_possible_keys:
                                  final_possible_keys.append("".join(tmp)) 
                                
                    print(final_possible_keys)
                    base_char=alphabets[lang][0]

                    # Calculate rotation
                    newernewertexts=[]
                    for key in final_possible_keys:
                        newertexts=[]
                        for i in range(len(newtexts)-1):
                            #print(i)
                            ntext=""
                            for ch in newtexts[i]:
                                ntext+=chr(((ord(ch)-ord(key[i])+26)%26 )+ 97)
                            newertexts.append(ntext)
                        newernewertexts.append(newertexts)

                    #finaltext =""
                    ##while  len(newertexts[0])>0:
                    ##   # print(f"{len(finaltext)}/{totalchar}")
                    ##    for i in range(0,len(newertexts)-1):
                    ##        finaltext+=newertexts[i][0]
                    ##        newertexts[i]=newertexts[i][1:]
                    #
                    ##for i in range(0,-1):
                    ##    for j in range(0,len(newertexts)-1):
                    ##        finaltext+=newertexts[j][i]
                    c = 0
                    for newertexts in newernewertexts: 

                        #print(len(newertexts))   
                        #for t in newertexts:
                        #   print(t[:50])
                        # print(newertexts[:50])
                        finaltext=""
                        while len(finaltext)<totalchar:
                           # print(len(newertexts))
                            #print(f"cur: {len(finaltext)}\ntar: {totalchar}")
                            for i in range(len(newertexts)):
                                if len(newertexts[i])>0:
                                    finaltext+=newertexts[i][0]
                                    newertexts[i]=newertexts[i][1:]
                            done = True

                            for text in newertexts:

                                if len(text)>0:
                                    done = False
                            #print("----")

                            if done:
                                break
                            
                        with open("cracked.txt","a") as f:
                            f.write(finaltext)
                            f.write("\n\n =======next key========\n\n")
                        c+=1

                case "0":
                    raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nBye :)")
        return 0

main()
