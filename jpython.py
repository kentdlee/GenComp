import jpythonscanner
import jpythonparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: jpython filename")
        print("   jpython will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = jpythonscanner.jpythonScanner(strm)
    theParser = jpythonparser.jpythonParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
