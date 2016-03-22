import calcscanner
import calcparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: calc filename")
        print("   calc will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = calcscanner.calcScanner(strm)
    theParser = calcparser.calcParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
