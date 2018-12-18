import classexamplescanner
import classexampleparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: classexample filename")
        print("   classexample will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = classexamplescanner.classexampleScanner(strm)
    theParser = classexampleparser.classexampleParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
