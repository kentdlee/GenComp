import exptermscanner
import exptermparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: expterm filename")
        print("   expterm will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = exptermscanner.exptermScanner(strm)
    theParser = exptermparser.exptermParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
