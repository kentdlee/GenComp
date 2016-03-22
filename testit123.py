import expressionscanner
import expressionparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: expc filename")
        print("   Expression compiler will interpret the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = expressionscanner.expressionScanner(strm)
    theParser = expressionparser.expressionParser()
    
    ast = theParser.parse(theScanner)
    print(ast.eval())
    
if __name__ == "__main__":
    main()
