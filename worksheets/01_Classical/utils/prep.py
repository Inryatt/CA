import sys
import unicodedata
import re
import time
def main():
    start_time = time.time()
    filen=sys.argv[1]

    with  open(filen,"r") as f:
        lines = f.readlines()

    out=""

    for line in lines:
        line=line.casefold().replace(" ","").strip() # remove spaces and set to lower case

        line = unicodedata.normalize("NFD",line)\
                .encode('ascii','ignore')\
                .decode('utf-8')
        line=re.sub('[^a-zA-Z]+', '',line)
        out+=line

    with open(filen+".out.txt","w+") as f:
        f.write(out)

    print("--- %s seconds ---" % (time.time() - start_time))


def prepare(lines):
    out=""
    for line in lines:
        line=line.casefold().replace(" ","").strip() # remove spaces and set to lower case

        line = unicodedata.normalize("NFD",line)\
                .encode('ascii','ignore')\
                .decode('utf-8')
        line=re.sub('[^a-zA-Z]+', '',line)
        out+=line

    return out

if __name__=="__main__":
    main()
