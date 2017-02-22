import listexpscanner
import listexpparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: listexp filename")
        print("   listexp will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = listexpscanner.listexpScanner(strm)
    theParser = listexpparser.listexpParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    print(ast.eval())
    
if __name__ == "__main__":
    main()
