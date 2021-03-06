import identifiersscanner
import identifiersparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: identifiers filename")
        print("   identifiers will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = identifiersscanner.identifiersScanner(strm)
    theParser = identifiersparser.identifiersParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
