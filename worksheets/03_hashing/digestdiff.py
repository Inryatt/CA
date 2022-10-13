import collections
import enum
import sys

def main():
    with open(sys.argv[1],'r') as f:
        digests = f.readlines()

    digests=[x.strip() for x in digests]
    results=[]
    for i in range(len(digests)):
        #print(digests[i])
        #print(f"{digests[i]}\n{digests[i+1]}")

        if i==len(digests)-1:
            break
        for k in range(len(digests)):
            count=0

            for j  in range(len(digests[i])):

                #print(digests[i][j])
                #print(digests[i+1][j])
                if digests[i]==digests[k]:
                    continue
                if digests[i][j]=='=':

                    break
                if digests[i][j]==digests[k][j]:
                    count+=1
            results.append(count/len(digests[0]))
        

    #results=[val/len(digests[0]) for val in results]
    multiplier=(1/len(results))*100
    results = collections.Counter(results)
    print(results)
    print("Similarity | Number of occurences")
    
    for result in results:
        print(f"{result:10.4} | "+ "".join(["=" for n in range(0,int(results[result]*multiplier))  ])   ) 
        
            
main()
