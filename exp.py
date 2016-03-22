import expscanner
import expparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: exp filename")
        print("   exp will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = expscanner.expScanner(strm)
    theParser = expparser.expParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
