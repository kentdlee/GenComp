import listscanner
import listparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: list filename")
        print("   list will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = listscanner.listScanner(strm)
    theParser = listparser.listParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
